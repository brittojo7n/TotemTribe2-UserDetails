from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def generate_user_url(user_id):
    return f'https://enkord.com/account/{user_id}'

def get_user_details(account_name, limit=500):  # Added a limit parameter with a default value of 50
    df = pd.read_csv('tt2_players.csv')
    account_name = account_name.strip().lower()

    if account_name.endswith('#'):
        account_name = account_name.rstrip('#')
        matching_names = df[df['Enkord account full name'].str.lower().str.startswith(account_name)]
        if not matching_names.empty:
            if len(matching_names) == 1:
                user_details = matching_names
                user_id = user_details['User ID'].iloc[0]
                url = generate_user_url(user_id)
                return user_details.to_html(index=False), url
            else:
                matches_with_links = []
                for idx, row in matching_names.sort_values(by='Enkord account full name').head(limit).iterrows():  # Use .head(limit) to limit the number of rows
                    user_id = row['User ID']
                    user_url = generate_user_url(user_id)
                    match_with_link = f'<a href="{user_url}">{row["Enkord account full name"]}</a>'
                    matches_with_links.append(match_with_link)
                matches_html = '<br>'.join(matches_with_links)
                return f'Multiple matches found:<br>{matches_html}', None
        else:
            return f'No exact match found for "{account_name}". Showing similar usernames.', None
    else:
        matching_names = df[df['Enkord account full name'].str.lower().str.contains(account_name)]
        if not matching_names.empty:
            if len(matching_names) == 1:
                user_details = matching_names
                user_id = user_details['User ID'].iloc[0]
                url = generate_user_url(user_id)
                return user_details.to_html(index=False), url
            else:
                matches_with_links = []
                for idx, row in matching_names.sort_values(by='Enkord account full name').head(limit).iterrows():  # Use .head(limit) to limit the number of rows
                    user_id = row['User ID']
                    user_url = generate_user_url(user_id)
                    match_with_link = f'<a href="{user_url}">{row["Enkord account full name"]}</a>'
                    matches_with_links.append(match_with_link)
                matches_html = '<br>'.join(matches_with_links)
                return f'Multiple matches found:<br>{matches_html}', None
        else:
            return f'No exact match found for "{account_name}". Showing similar usernames.', None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        account_name = request.form['account_name'].strip()  # Strip leading/trailing whitespace
        if not account_name:
            error_message = 'Please enter a valid account name.'
            return render_template('index.html', user_details=None, url=None, account_name=None, error_message=error_message)
        
        user_details, url = get_user_details(account_name)
        return render_template('index.html', user_details=user_details, url=url, account_name=account_name)
    else:
        return render_template('index.html', user_details=None, url=None, account_name=None, error_message=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
