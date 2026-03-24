from flask import Flask, request, jsonify, render_template
import json
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/show-ip', methods=['GET'])
def show_ip():
    try:
        response = requests.get('https://api.ipify.org/', timeout=10)
        return jsonify({'success': True, 'ip': response.text})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/ip-track', methods=['POST'])
def ip_track():
    data = request.get_json()
    ip = data.get('ip', '').strip()
    if not ip:
        return jsonify({'success': False, 'error': 'IP address is required'}), 400
    try:
        req_api = requests.get(f'http://ipwho.is/{ip}', timeout=10)
        ip_data = req_api.json()
        if not ip_data.get('success', True):
            return jsonify({'success': False, 'error': ip_data.get('message', 'Invalid IP')}), 400

        lat = ip_data.get('latitude', 0)
        lon = ip_data.get('longitude', 0)
        result = {
            'ip': ip,
            'type': ip_data.get('type'),
            'country': ip_data.get('country'),
            'country_code': ip_data.get('country_code'),
            'city': ip_data.get('city'),
            'continent': ip_data.get('continent'),
            'continent_code': ip_data.get('continent_code'),
            'region': ip_data.get('region'),
            'region_code': ip_data.get('region_code'),
            'latitude': lat,
            'longitude': lon,
            'maps': f'https://www.google.com/maps/@{lat},{lon},8z',
            'is_eu': ip_data.get('is_eu'),
            'postal': ip_data.get('postal'),
            'calling_code': ip_data.get('calling_code'),
            'capital': ip_data.get('capital'),
            'borders': ip_data.get('borders'),
            'flag': ip_data.get('flag', {}).get('emoji'),
            'asn': ip_data.get('connection', {}).get('asn'),
            'org': ip_data.get('connection', {}).get('org'),
            'isp': ip_data.get('connection', {}).get('isp'),
            'domain': ip_data.get('connection', {}).get('domain'),
            'timezone_id': ip_data.get('timezone', {}).get('id'),
            'timezone_abbr': ip_data.get('timezone', {}).get('abbr'),
            'is_dst': ip_data.get('timezone', {}).get('is_dst'),
            'utc_offset': ip_data.get('timezone', {}).get('offset'),
            'utc': ip_data.get('timezone', {}).get('utc'),
            'current_time': ip_data.get('timezone', {}).get('current_time'),
        }
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phone-track', methods=['POST'])
def phone_track():
    data = request.get_json()
    phone = data.get('phone', '').strip()
    if not phone:
        return jsonify({'success': False, 'error': 'Phone number is required'}), 400
    try:
        default_region = 'ID'
        parsed = phonenumbers.parse(phone, default_region)
        region_code = phonenumbers.region_code_for_number(parsed)
        carrier_name = carrier.name_for_number(parsed, 'en')
        location = geocoder.description_for_number(parsed, 'id')
        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)
        intl_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        mobile_format = phonenumbers.format_number_for_mobile_dialing(parsed, default_region, with_formatting=True)
        e164_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        number_type = phonenumbers.number_type(parsed)
        timezones = ', '.join(timezone.time_zones_for_number(parsed))

        if number_type == phonenumbers.PhoneNumberType.MOBILE:
            type_str = 'Mobile'
        elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
            type_str = 'Fixed Line'
        else:
            type_str = 'Other'

        result = {
            'location': location,
            'region_code': region_code,
            'timezone': timezones,
            'carrier': carrier_name,
            'is_valid': is_valid,
            'is_possible': is_possible,
            'international_format': intl_format,
            'mobile_format': mobile_format,
            'national_number': str(parsed.national_number),
            'e164': e164_format,
            'country_code': parsed.country_code,
            'type': type_str,
        }
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/username-track', methods=['POST'])
def username_track():
    data = request.get_json()
    username = data.get('username', '').strip()
    if not username:
        return jsonify({'success': False, 'error': 'Username is required'}), 400

    social_media = [
        {'url': 'https://www.facebook.com/{}', 'name': 'Facebook'},
        {'url': 'https://www.twitter.com/{}', 'name': 'Twitter'},
        {'url': 'https://www.instagram.com/{}', 'name': 'Instagram'},
        {'url': 'https://www.linkedin.com/in/{}', 'name': 'LinkedIn'},
        {'url': 'https://www.github.com/{}', 'name': 'GitHub'},
        {'url': 'https://www.pinterest.com/{}', 'name': 'Pinterest'},
        {'url': 'https://www.tumblr.com/{}', 'name': 'Tumblr'},
        {'url': 'https://www.youtube.com/{}', 'name': 'YouTube'},
        {'url': 'https://soundcloud.com/{}', 'name': 'SoundCloud'},
        {'url': 'https://www.snapchat.com/add/{}', 'name': 'Snapchat'},
        {'url': 'https://www.tiktok.com/@{}', 'name': 'TikTok'},
        {'url': 'https://www.behance.net/{}', 'name': 'Behance'},
        {'url': 'https://www.medium.com/@{}', 'name': 'Medium'},
        {'url': 'https://www.quora.com/profile/{}', 'name': 'Quora'},
        {'url': 'https://www.flickr.com/people/{}', 'name': 'Flickr'},
        {'url': 'https://www.twitch.tv/{}', 'name': 'Twitch'},
        {'url': 'https://www.dribbble.com/{}', 'name': 'Dribbble'},
        {'url': 'https://www.ello.co/{}', 'name': 'Ello'},
        {'url': 'https://www.producthunt.com/@{}', 'name': 'Product Hunt'},
        {'url': 'https://www.telegram.me/{}', 'name': 'Telegram'},
        {'url': 'https://www.weheartit.com/{}', 'name': 'We Heart It'},
    ]

    results = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})

    for site in social_media:
        url = site['url'].format(username)
        try:
            response = session.get(url, timeout=8, allow_redirects=True)
            found = response.status_code == 200
        except Exception:
            found = False
        results.append({'name': site['name'], 'url': url, 'found': found})

    return jsonify({'success': True, 'username': username, 'results': results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
