import plotly.express as px
import pandas as pd
import numpy as np

# update/add code below ...

def survival_demographics(df):
    """
    Analyze survival patterns by passenger class, sex, and age group.
    
    Args:
        df: DataFrame containing Titanic passenger data
        
    Returns:
        DataFrame with survival statistics by demographic groups
    """
    # Create age groups as categorical
    bins = [0, 12, 19, 59, np.inf]
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    df['age_group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    # Group by class, sex, and age group
    grouped = df.groupby(['Pclass', 'Sex', 'age_group'], dropna=False)
    
    # Calculate statistics
    result = grouped.agg(
        n_passengers=('PassengerId', 'count'),
        n_survivors=('Survived', 'sum')
    ).reset_index()
    
    # Create all combinations to include groups with no members
    all_combos = pd.MultiIndex.from_product(
        [[1, 2, 3], ['female', 'male'], labels],
        names=['Pclass', 'Sex', 'age_group']
    ).to_frame(index=False)
    
    # Merge and fill missing groups with 0
    result = (all_combos
              .merge(result, how='left', on=['Pclass', 'Sex', 'age_group'])
              .fillna({'n_passengers': 0, 'n_survivors': 0}))
    result['n_passengers'] = result['n_passengers'].astype(int)
    result['n_survivors'] = result['n_survivors'].astype(int)
    
    # Calculate survival rate, and handle division
    result['survival_rate'] = result['n_survivors'] / result['n_passengers'].replace(0, np.nan)
    result['survival_rate'] = result['survival_rate'].fillna(0)
    
    # Sort for better readability
    result = result.sort_values(['Pclass', 'Sex', 'age_group'])
    
    return result


def visualize_demographic():
    """
    Visualize survival rates across different age groups.
    
    Returns:
        Plotly figure showing survival patterns
    """
    # Load data
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    
    # Get survival demographics
    data = survival_demographics(df)
    
    # Calculate average survival rate for each age group (across all classes and sexes)
    avg_by_age = data.groupby('age_group').agg(
        avg_survival_rate=('survival_rate', 'mean')
    ).reset_index()
    
    # Simple bar chart
    fig = px.bar(
        avg_by_age,
        x='age_group',
        y='avg_survival_rate',
        color='age_group',
    )

    fig.update_layout(
        title='Average Survival Rates by Age Group',
        xaxis_title='Age Group',
        yaxis_title='Average Survival Rate',
    )
    # Change the survival rates to percentages instead of decimals
    fig.update_yaxes(tickformat='.0%')
    
    return fig

visualize_demographic()