from flask import Flask, render_template, request, session
from flask_session import Session
import scraper as sc
import ai as ai

reportapp = Flask(__name__)
reportapp.secret_key = '6ab4d1f48eb8db844a9d6ee6ee18a9565950802b993ef0f6'
reportapp.config['SESSION_TYPE'] = 'filesystem'
Session(reportapp)

@reportapp.route('/')
def home():
    return render_template('index.html')

@reportapp.route('/generate', methods=['POST'])
def generate_output():
    topic = request.form['topic']
    session['topic'] = topic

    google_results = sc.perform_google_search(topic)
    bullet_summaries = []
    content_ideas = []
    twitter_tweets = []
    total_token_count = 0
    session['bullet_summaries'] = bullet_summaries
    session['content_ideas'] = content_ideas
    session['twitter_tweets'] = twitter_tweets
    session['total_token_count'] = total_token_count
    
    for result in google_results:
        article = sc.get_article_from_url(result["url"])
        bullet_summary = ai.blog_post_to_bullet_points(article)
        if bullet_summary:
            bullet_summaries.append(bullet_summary)
            total_token_count += ai.count_tokens(bullet_summary)
            ideas = ai.generate_content_ideas(bullet_summary)
            content_ideas.append(ideas)
            total_token_count += ai.count_tokens(ideas)
            tweets = ai.generate_tweets(bullet_summary)
            twitter_tweets.append(tweets)
            total_token_count += ai.count_tokens(tweets)

    thousands_chunks = total_token_count / 1000
    estimate_cost = thousands_chunks * 0.002
    session['estimate_cost'] = estimate_cost

    bullet_summaries = bullet_summaries[:10]
    content_ideas = content_ideas[:10]
    twitter_tweets = twitter_tweets[:10]

    return render_template('output.html', topic=topic, bullet_summaries=bullet_summaries,
                           content_ideas=content_ideas, twitter_tweets=twitter_tweets,
                           estimate_cost=estimate_cost, total_token_count=total_token_count)

# @reportapp.route('/download_pdf')
# def download_pdf():
#     topic = session.get('topic')
#     bullet_summaries = session.get('bullet_summaries', [])[:10]
#     content_ideas = session.get('content_ideas', [])[:10]
#     twitter_tweets = session.get('twitter_tweets', [])[:10]
#     estimate_cost = session.get('estimate_cost')
#     total_token_count = session.get('total_token_count')

#     pdf_output = rp.generate_pdf_report(topic, bullet_summaries, content_ideas, twitter_tweets, estimate_cost, total_token_count)

#     if pdf_output:
#         return send_file(
#             io.BytesIO(pdf_output.getvalue()),
#             as_attachment=True,
#             download_name='output.pdf',
#             mimetype='application/pdf'
#         )
#     else:
#         return "PDF report not found."

@reportapp.route('/styles.css')
def serve_css():
    return reportapp.send_static_file('styles.css')

if __name__ == '__main__':
    reportapp.run()
