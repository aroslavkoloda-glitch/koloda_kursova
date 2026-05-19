import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Оцінка стійкості мережі", layout="wide")
st.title("🛡️ Оцінка стійкості мережі до відмов вузлів")

G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 5), (6, 7)])

st.sidebar.header("⚙️ Налаштування")
failed_node = st.sidebar.selectbox("Виберіть вузол для відмови", list(G.nodes()))

if st.sidebar.button("🚨 СИМУЛЮВАТИ ВІДМОВУ"):
    G_failed = G.copy()
    G_failed.remove_node(failed_node)
    
    if G_failed.number_of_nodes() > 0:
        largest = max(nx.connected_components(G_failed), key=len)
        resilience = len(largest) / G.number_of_nodes()
    else:
        resilience = 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Всього вузлів", G.number_of_nodes())
    col2.metric("❌ Відмовлено", failed_node)
    col3.metric("🟢 Стійкість", f"{resilience:.0%}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=14, ax=ax1)
    ax1.set_title("✅ Початкова мережа")
    
    colors = ['lightgreen' if n in largest else 'salmon' for n in G_failed.nodes()]
    nx.draw(G_failed, pos, with_labels=True, node_color=colors, node_size=800, font_size=14, ax=ax2)
    ax2.set_title(f"❌ Після відмови вузла {failed_node}")
    
    st.pyplot(fig)
else:
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=14, ax=ax)
    ax.set_title("Топологія мережі")
    st.pyplot(fig)

st.caption("Курсова робота: Оцінка стійкості мережі до відмов вузлів")
