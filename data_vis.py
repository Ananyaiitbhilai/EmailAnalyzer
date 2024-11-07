import plotly.graph_objects as go
import plotly.utils
import json
from collections import defaultdict

def create_toxicity_pie_chart(toxic_count, total_count):
    non_toxic_count = total_count - toxic_count
    
    fig = go.Figure(data=[go.Pie(
        labels=['Toxic', 'Non-toxic'],
        values=[toxic_count, non_toxic_count],
        hole=.3,
        marker_colors=['#ff9999', '#66b3ff']
    )])
    
    fig.update_layout(
        title="Distribution of Toxic vs Non-toxic Emails",
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=0, r=0, b=0)
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def process_toxicity_categories(emails):
    categories_data = defaultdict(float)
    
    for email in emails:
        if not email.get('Non-toxic', True):  # Only process toxic emails
            for category, subcats in email.get('toxic', {}).items():
                if isinstance(subcats, dict):
                    for subcat, value in subcats.items():
                        if value > 0:
                            full_category = f"{category}: {subcat}"
                            categories_data[full_category] += value
                elif isinstance(subcats, (int, float)) and subcats > 0:
                    categories_data[category] += subcats
    
    # Filter out categories with 0 values
    return {k: v for k, v in categories_data.items() if v > 0}

def create_category_bar_chart(emails):
    categories_data = process_toxicity_categories(emails)
    
    # Add debug logging
    print(f"Categories data: {categories_data}")
    
    # Sort categories by value
    sorted_categories = sorted(categories_data.items(), key=lambda x: x[1], reverse=True)
    categories = [x[0] for x in sorted_categories]
    values = [x[1] for x in sorted_categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color='#ff9999'
        )
    ])
    
    fig.update_layout(
        title="Distribution of Toxicity Categories",
        title_x=0.5,
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=0, r=0, b=150),  # Increased bottom margin for labels
        height=600,
        yaxis_title="Count",
        xaxis_title="Category"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def process_sender_category_data(emails):
    sender_category_data = []
    
    for email in emails:
        if not email.get('Non-toxic', True):  # Only process toxic emails
            sender = email.get('sender_name', '').split('<')[0].strip()  # Get name part before email
            
            for category, subcats in email.get('toxic', {}).items():
                if isinstance(subcats, dict):
                    for subcat, value in subcats.items():
                        if value > 0:
                            full_category = f"{category}: {subcat}"
                            sender_category_data.append((sender, full_category, value))
                elif isinstance(subcats, (int, float)) and subcats > 0:
                    sender_category_data.append((sender, category, subcats))
    
    return sender_category_data

def create_sender_sankey(emails):
    sender_category_data = process_sender_category_data(emails)
    
    if not sender_category_data:
        # Return empty figure if no data
        return json.dumps(go.Figure(), cls=plotly.utils.PlotlyJSONEncoder)
    
    # Get unique senders and categories
    senders = list(set(item[0] for item in sender_category_data))
    categories = list(set(item[1] for item in sender_category_data))
    
    # Create source and target indices
    source = [senders.index(item[0]) for item in sender_category_data]
    target = [len(senders) + categories.index(item[1]) for item in sender_category_data]
    value = [item[2] for item in sender_category_data]
    
    # Create labels and colors
    node_labels = senders + categories
    node_colors = ['#1f77b4'] * len(senders) + ['#ff7f0e'] * len(categories)
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    )])
    
    fig.update_layout(
        title="Flow of Toxicity from Senders to Categories",
        title_x=0.5,
        font_size=10,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=800
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_relationship_analysis_chart(emails):
    # Count different types of relationships
    relationship_counts = defaultdict(int)
    for email in emails:
        relationships = email.get('relationship_analysis', {}).get('relationship_analysis', {})
        for rel_type, value in relationships.items():
            if value == 1:
                relationship_counts[rel_type] += 1
    
    # Create the bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=list(relationship_counts.keys()),
            y=list(relationship_counts.values()),
            marker_color='#2ecc71'
        )
    ])
    
    fig.update_layout(
        title="Distribution of Relationship Types in Emails",
        title_x=0.5,
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=0, r=0, b=150),
        height=500,
        yaxis_title="Count",
        xaxis_title="Relationship Type"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)