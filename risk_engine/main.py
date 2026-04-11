import os
from src.predict import (
    load_data,
    validate_data,
    predict_risk,
    aggregate_issue_priorities,
    generate_explanations,
)
from src.recommender import generate_recommendations


def run():
    df = load_data()
    validate_data(df)
    df = predict_risk(df)

    priority_df = aggregate_issue_priorities(df)
    priority_df = generate_explanations(priority_df)
    priority_df = generate_recommendations(priority_df)

    # Save output
    os.makedirs("output", exist_ok=True)
    output_path = "output/final_recommendations.csv"
    priority_df.to_csv(output_path, index=False)

    print("\n🚀 FINAL DECISION ENGINE OUTPUT:\n")
    print(f"Saved to: {output_path}\n")

    print("Top 5 Issues with Recommendations:\n")

    for _, row in priority_df.head(5).iterrows():
        print(f"Machine: {row['machine_id']}")
        print(f"Issue: {row['reason']}")
        print(f"Priority Score: {round(row['priority_score'], 2)}")
        print(f"Why: {row['explanation']}")
        print(f"Likely Cause: {row['likely_cause']}")
        print(f"Recommended Actions: {row['recommended_actions']}")
        print("-" * 50)


if __name__ == "__main__":
    run()