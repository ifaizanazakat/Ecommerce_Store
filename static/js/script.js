function analyzeReview() {
    const review = document.getElementById("review-input").value;
    fetch("/analyze_reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reviews: [review] }),
    })
    .then((response) => response.json())
    .then((data) => {
        const resultDiv = document.getElementById("analysis-result");
        resultDiv.innerHTML = `<p>Sentiment Score: ${data[0].sentiment} (Score: ${data[0].score})`;

        // Set the review for submission
        document.getElementById("review").value = review;
    })
    .catch((error) => console.error("Error:", error));
}
