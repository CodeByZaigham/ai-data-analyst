import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
)

st.sidebar.title("⚙️ Settings")

backend_url = st.sidebar.text_input(
    "Backend URL",
    value=st.session_state.get("backend_url", "http://127.0.0.1:8000"),
    help="Base URL of your FastAPI backend (no trailing slash).",
).rstrip("/")
st.session_state["backend_url"] = backend_url

if st.sidebar.button("🔌 Test connection"):
    try:
        r = requests.get(f"{backend_url}/", timeout=5)
        if r.ok:
            st.sidebar.success(f"Connected: {r.json().get('msg', 'ok')}")
        else:
            st.sidebar.error(f"Backend responded with status {r.status_code}")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Could not reach backend: {e}")

st.sidebar.markdown("---")
st.sidebar.subheader("🕘 Query History")

if "history" not in st.session_state:
    st.session_state["history"] = []  # list of dicts: question, sql, data, description

if st.session_state["history"]:
    for i, item in enumerate(reversed(st.session_state["history"])):
        if st.sidebar.button(f"• {item['question'][:40]}", key=f"hist_{i}"):
            st.session_state["active_result"] = item
else:
    st.sidebar.caption("No queries yet.")

if st.sidebar.button("🗑️ Clear history"):
    st.session_state["history"] = []
    st.session_state.pop("active_result", None)
    st.rerun()

st.title("📊 AI Data Analyst")
st.caption(
    "Ask a question about your database in plain English — get the SQL, "
    "the data, a summary, and a chart, automatically."
)

with st.form(key="query_form"):
    question = st.text_input(
        "Ask a question about your data",
        placeholder="e.g. Which city generates the most revenue and how does customer behavior differ by city?",
    )
    submitted = st.form_submit_button("🚀 Analyze", use_container_width=True)

if submitted:
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking, generating SQL, and analyzing data..."):
            try:
                resp = requests.post(
                    f"{backend_url}/query",
                    json={"question": question},
                    timeout=60,
                )
                if resp.status_code == 200:
                    result = resp.json()

                    # Backend can return either the expected llm_response
                    # shape, or (on internal errors) a plain error string.
                    if isinstance(result, dict) and "Sqlquery" in result:
                        entry = {
                            "question": question,
                            "sql": result.get("Sqlquery", ""),
                            "data": result.get("Data", []),
                            "description": result.get("Description", ""),
                        }
                        st.session_state["history"].append(entry)
                        st.session_state["active_result"] = entry
                    else:
                        st.error(f"Backend error: {result}")
                else:
                    st.error(f"Request failed with status {resp.status_code}: {resp.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not reach backend at {backend_url}. Error: {e}")

def auto_visualize(df: pd.DataFrame):
    """
    Inspect the dataframe's columns and dtypes, then pick a sensible
    matplotlib chart automatically:
      - 1 categorical + 1 numeric        -> bar chart
      - 1 categorical + multiple numeric -> grouped bar chart
      - date/time + numeric              -> line chart
      - 2 numeric only                   -> scatter plot
      - 1 numeric only                   -> histogram
      - otherwise                        -> no chart
    """
    if df.empty or df.shape[0] < 1:
        st.info("No data to visualize.")
        return

    df = df.copy()

    id_pattern = re.compile(r"(^id$)|(_id$)|(^uuid$)", re.IGNORECASE)
    id_cols = [c for c in df.columns if id_pattern.search(c)]
    plottable_df = df.drop(columns=id_cols) if len(id_cols) < len(df.columns) else df

    date_col = None
    for col in plottable_df.columns:
        if "date" in col.lower() or "time" in col.lower():
            try:
                converted = pd.to_datetime(plottable_df[col], errors="coerce")
                if converted.notna().sum() > 0:
                    date_col = col
                    plottable_df[col] = converted
                    break
            except Exception:
                pass

    numeric_cols = plottable_df.select_dtypes(include="number").columns.tolist()
    for col in plottable_df.columns:
        if col not in numeric_cols and col != date_col:
            coerced = pd.to_numeric(plottable_df[col], errors="coerce")
            if coerced.notna().sum() == len(plottable_df) and coerced.notna().sum() > 0:
                plottable_df[col] = coerced
                numeric_cols.append(col)

    categorical_cols = [
        c for c in plottable_df.columns if c not in numeric_cols and c != date_col
    ]

    if not numeric_cols:
        st.info("Couldn't find a numeric column to chart — showing table only.")
        return

    plot_cols = numeric_cols[:4]

    scales_differ = False
    if len(plot_cols) > 1:
        maxes = [plottable_df[c].abs().max() or 1 for c in plot_cols]
        scales_differ = (max(maxes) / max(min(maxes), 1e-9)) > 15

    try:
        if date_col and plot_cols:
            if scales_differ:
                fig, axes = plt.subplots(
                    len(plot_cols), 1, figsize=(9, 3 * len(plot_cols)), sharex=True
                )
                axes = axes if hasattr(axes, "__iter__") else [axes]
                df_sorted = plottable_df.sort_values(date_col)
                for ax, col in zip(axes, plot_cols):
                    ax.plot(df_sorted[date_col], df_sorted[col], marker="o", color="#4C72B0")
                    ax.set_ylabel(col)
                    ax.set_title(col)
                axes[-1].set_xlabel(date_col)
                fig.autofmt_xdate()
            else:
                fig, ax = plt.subplots(figsize=(9, 5))
                df_sorted = plottable_df.sort_values(date_col)
                for col in plot_cols:
                    ax.plot(df_sorted[date_col], df_sorted[col], marker="o", label=col)
                ax.set_xlabel(date_col)
                ax.set_title(f"{', '.join(plot_cols)} over {date_col}")
                fig.autofmt_xdate()
                if len(plot_cols) > 1:
                    ax.legend()

        elif categorical_cols and plot_cols:
            cat_col = categorical_cols[0]
            labels = plottable_df[cat_col].astype(str)

            if len(plot_cols) == 1:
                fig, ax = plt.subplots(figsize=(9, 5))
                ax.bar(labels, plottable_df[plot_cols[0]], color="#4C72B0")
                ax.set_ylabel(plot_cols[0])
                ax.set_xlabel(cat_col)
                ax.set_title(f"{plot_cols[0]} by {cat_col}")
                plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

            elif scales_differ:
                fig, axes = plt.subplots(
                    len(plot_cols), 1, figsize=(9, 3 * len(plot_cols)), sharex=True
                )
                axes = axes if hasattr(axes, "__iter__") else [axes]
                colors = plt.cm.tab10.colors
                for i, (ax, col) in enumerate(zip(axes, plot_cols)):
                    ax.bar(labels, plottable_df[col], color=colors[i % len(colors)])
                    ax.set_ylabel(col)
                    ax.set_title(col)
                plt.setp(axes[-1].get_xticklabels(), rotation=30, ha="right")
                axes[-1].set_xlabel(cat_col)

            else:
                fig, ax = plt.subplots(figsize=(9, 5))
                x = range(len(plottable_df))
                width = 0.8 / len(plot_cols)
                for i, col in enumerate(plot_cols):
                    ax.bar(
                        [p + i * width for p in x],
                        plottable_df[col],
                        width=width,
                        label=col,
                    )
                ax.set_xticks([p + width * (len(plot_cols) - 1) / 2 for p in x])
                ax.set_xticklabels(labels)
                ax.legend()
                ax.set_xlabel(cat_col)
                ax.set_title(f"{', '.join(plot_cols)} by {cat_col}")
                plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

        elif len(plot_cols) >= 2:
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.scatter(plottable_df[plot_cols[0]], plottable_df[plot_cols[1]], color="#4C72B0")
            ax.set_xlabel(plot_cols[0])
            ax.set_ylabel(plot_cols[1])
            ax.set_title(f"{plot_cols[1]} vs {plot_cols[0]}")

        else:
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.hist(
                plottable_df[plot_cols[0]].dropna(),
                bins=min(20, max(5, plottable_df.shape[0])),
                color="#4C72B0",
            )
            ax.set_xlabel(plot_cols[0])
            ax.set_ylabel("Frequency")
            ax.set_title(f"Distribution of {plot_cols[0]}")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        plt.close("all")
        st.info(f"Couldn't generate a chart automatically for this data ({e}).")

active = st.session_state.get("active_result")

if active:
    st.markdown("---")
    st.subheader(f"❓ {active['question']}")

    tab_summary, tab_data, tab_chart, tab_sql = st.tabs(
        ["📝 Summary", "📋 Data", "📈 Visualization", "🧾 SQL"]
    )

    data = active["data"]

    with tab_summary:
        if active["description"]:
            st.write(active["description"])
        else:
            st.info("No description returned.")

    with tab_data:
        if isinstance(data, list) and data and isinstance(data[0], dict):
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            st.download_button(
                "⬇️ Download as CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="query_result.csv",
                mime="text/csv",
            )
        else:
            st.write(data)

    with tab_chart:
        if isinstance(data, list) and data and isinstance(data[0], dict):
            df_chart = pd.DataFrame(data)
            auto_visualize(df_chart)
        else:
            st.info("No tabular data available to visualize.")

    with tab_sql:
        st.code(active["sql"], language="sql")

else:
    st.markdown("---")
    st.info("👋 Ask a question above to get started. Make sure your FastAPI backend is running.")