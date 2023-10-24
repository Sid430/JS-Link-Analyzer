import openai
import os
import sys

try:
    openai.api_key = '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'
except KeyError:
    sys.stderr.write("BAD")
    exit(1)

# Define the path to the "Downloads" folder
downloads_folder = os.path.expanduser("~") + '/Downloads/'

# Input and output file paths
input_file_path = os.path.join(downloads_folder, 'links.txt')  # Full path to links.txt
output_file_path = os.path.join(downloads_folder, 'output.txt')  # Full path to output.txt
non_unknown_links_file_path = os.path.join(downloads_folder, 'non_unknown_links.txt')  # Full path to non_unknown_links.txt

# Read links from the input file
with open(input_file_path, 'r') as input_file:
    links = input_file.readlines()

# Initialize an empty set to store unique companies
unique_companies = set()
non_unknown_links = []

# Iterate through each link
for link in links:
    link = link.strip()  # Remove leading and trailing whitespaces
    if link:
        # Run the OpenAI API on the current link
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful link-analyzer who only responds with one word (do not add periods to the end of that word). Note: If you cannot determine or the link is unknown, do not return anything (just a blank). Never return Unknown or a similar version."},
                {"role": "user", "content": f"What company is featured in: {link}"},
            ],
            timeout=2400
        )

        # Extract assistant's reply
        assistant_reply = response['choices'][0]['message']['content']

        # If the reply is not "unknown" or similar, add the link to the non_unknown_links list
        if assistant_reply not in ["unknown", "Unknown", "unknown.", "Unknown.", "blank", "Blank", "blank.", "Blank.", "undetermined", "Undetermined", "Unspecified", "Unspecified.", "unspecified", "unspecified.", "Impossible", "impossible", "Impossible.", "impossible."]:
            non_unknown_links.append(link)

        # Add the company to the set (set automatically handles duplicates)
        unique_companies.add(assistant_reply)

# Convert the set to a list for writing to the output file
unique_companies_list = list(unique_companies)

# Remove entries with "unknown" or "Unknown"
filtered_companies = [company for company in unique_companies_list if company.lower() not in ["unknown", "Unknown", "unknown.", "Unknown.", "blank", "Blank", "blank.", "Blank.", "undetermined", "Undetermined"]]

# Write the results to the output file
with open(output_file_path, 'w') as output_file:
    for company in filtered_companies:
        output_file.write(company + '\n')

# Write non-unknown links to a separate file
with open(non_unknown_links_file_path, 'w') as non_unknown_links_file:
    for link in non_unknown_links:
        non_unknown_links_file.write(link + '\n')

print("Processing complete. Unique companies (excluding 'unknown' and 'Unknown') written to", output_file_path)
print("Non-unknown links written to", non_unknown_links_file_path)



import urllib.request
import re

def search_and_save(url, keywords, found_terms):
    # Fetch the content of the web page
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch the web page {url}: {e}")
        return

    # Search for keywords in the text content
    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', html_content, re.IGNORECASE):
            found_terms.add(keyword)

    print(f"Search completed for {url}")

# Read URLs from a text file
with open(input_file_path, 'r') as input_file:
    links = input_file.readlines()

search_keywords = personal_identifiers = ["phone", "name", "address", "location", "phone_number", "phone", "mobile_number", "cell_number", "telephone", "contact_number", "fax_number", "ip_address", "ip", "email", "email_address", "ssn", "social_security_number", "credit_card", "credit_card_number", "bank_account", "bank_account_number", "username", "password", "passport", "passport_number", "driver_license", "driver_license_number", "address", "home_address", "work_address", "url", "web_address", "personal_id", "employee_id", "customer_id", "student_id", "date_of_birth", "dob", "full_name", "name", "gender", "ethnicity", "national_id", "tax_id", "voter_id", "user_id", "account_number", "social_media_handle", "biometric_data", "marital_status", "license_plate", "vehicle_registration", "organization_id", "organization_name", "organization_code", "school_id", "university_id", "library_card", "membership_id", "certificate_number", "transaction_id", "transaction_code", "client_id", "case_number", "court_docket", "medical_record_number", "insurance_policy_number", "patient_id", "subscriber_id","vendor_id", "serial_number", "tracking_number", "package_id", "parcel_number", "order_id", "invoice_number", "purchase_order", "reservation_id", "flight_number", "booking_reference", "ticket_number", "event_id", "event_code", "meeting_id", "conference_id", "session_id", "session_code", "reference_number", "reference_code", "record_id", "record_code", "file_number", "file_code", "project_id", "project_code", "task_id", "task_code", "assignment_id", "assignment_code", "product_id", "product_code", "sku", "upc", "ean", "isbn", "model_number", "manufacturer_id", "manufacturer_code", "supplier_id", "supplier_code", "partner_id", "partner_code", "affiliate_id", "affiliate_code", "sponsor_id", "sponsor_code", "employee_social_security_number", "employee_email", "employee_phone_number", "customer_social_security_number", "customer_email", "customer_phone_number", "vendor_social_security_number", "vendor_email", "vendor_phone_number", "supplier_social_security_number", "supplier_email", "supplier_phone_number", "contractor_social_security_number", "contractor_email", "contractor_phone_number", "subscriber_social_security_number", "subscriber_email", "subscriber_phone_number", "patient_social_security_number", "patient_email", "patient_phone_number", "student_social_security_number", "student_email", "student_phone_number", "user_social_security_number", "user_email", "user_phone_number", "citizen_social_security_number", "citizen_email", "citizen_phone_number", "resident_social_security_number", "resident_email", "resident_phone_number", "client_social_security_number", "client_email", "client_phone_number", "applicant_social_security_number", "applicant_email", "applicant_phone_number", "member_social_security_number", "member_email", "member_phone_number", "patient_name", "customer_name", "employee_name", "vendor_name", "supplier_name", "contractor_name", "subscriber_name", "student_name", "user_name", "citizen_name", "resident_name", "client_name", "applicant_name", "member_name", "organization_social_security_number", "organization_email", "organization_phone_number", "organization_name", "organization_code", "organization_id", "school_social_security_number", "school_email", "school_phone_number", "school_name", "school_code", "school_id", "university_social_security_number", "university_email", "university_phone_number", "university_name", "university_code", "university_id", "government_social_security_number", "government_email", "government_phone_number", "government_name", "government_code", "government_id", "court_social_security_number", "court_email", "court_phone_number", "court_name", "court_code", "court_id", "library_social_security_number", "library_email", "library_phone_number", "library_name", "library_code", "library_id", "club_social_security_number", "club_email", "club_phone_number", "club_name", "club_code", "club_id", "association_social_security_number", "association_email", "association_phone_number", "association_name", "association_code", "association_id", "membership_social_security_number", "membership_email", "membership_phone_number", "membership_name", "membership_code", "membership_id","certificate_social_security_number", "certificate_email", "certificate_phone_number", "certificate_name", "certificate_code", "certificate_id", "transaction_social_security_number", "transaction_email", "transaction_phone_number", "transaction_name", "transaction_code", "transaction_id", "record_social_security_number", "record_email", "record_phone_number", "record_name", "record_code", "record_id", "file_social_security_number", "file_email", "file_phone_number", "file_name", "file_code", "file_id", "project_social_security_number", "project_email", "project_phone_number", "project_name", "project_code", "project_id", "task_social_security_number", "task_email", "task_phone_number", "task_name", "task_code", "task_id", "assignment_social_security_number", "assignment_email", "assignment_phone_number", "assignment_name", "assignment_code", "assignment_id", "product_social_security_number", "product_email", "product_phone_number", "product_name", "product_code""shipment_location", "payment_location",
"purchase_location",
"order_location",
"account_location",
"customer_location",
"client_location",
"user_location",
"member_location",
"employee_location",
"partner_location",
"vendor_location",
"supplier_location",
"contractor_location",
"subscriber_location",
"patient_location",
"student_location",
"organization_location",
"school_location",
"university_location",
"government_location",
"court_location",
"library_location",
"club_location",
"association_location",
"membership_location",
"certificate_location",
"transaction_location",
"record_location",
"file_location",
"project_location",
"task_location",
"assignment_location",
"coupon_location",
"discount_location",
"promo_location",
"gift_card_location",
"loyalty_location",
"reward_location",
"membership_location",
"certificate_location",
"invoice_location",
"shipment_location",
"payment_location",
"purchase_location",
"order_location",
"account_location",
"customer_location",
"client_location",
"user_location",
"member_location",
"employee_location",
"partner_location",
"vendor_location", "purchase_id",
"order_number",
"order_reference",
"invoice_id",
"invoice_reference",
"shipping_id",
"tracking_code",
"shipment_id",
"payment_id",
"transaction_reference",
"subscription_id",
"subscription_code",
"loyalty_card_number",
"loyalty_program_id",
"loyalty_points",
"loyalty_member_id",
"loyalty_level",
"coupon_code",
"discount_code",
"promo_code",
"gift_card_number",
"gift_certificate_number",
"reward_points",
"membership_card_number",
"membership_level",
"account_username",
"account_email",
"account_id",
"customer_username",
"customer_email",
"customer_id",
"client_username",
"client_email",
"client_id",
"user_username",
"user_email",
"user_id",
"member_username",
"member_email",
"member_id",
"employee_username",
"employee_email",
"employee_id",
"partner_username",
"partner_email",
"partner_id",
"vendor_username",
"vendor_email",
"vendor_id",
"supplier_username",
"supplier_email",
"supplier_id",
"contractor_username",
"contractor_email",
"contractor_id",
"subscriber_username",
"subscriber_email",
"subscriber_id",
"patient_username",
"patient_email",
"patient_id",
"student_username",
"student_email",
"student_id",
"organization_username",
"organization_email",
"organization_id",
"school_username",
"school_email",
"school_id",
"university_username",
"university_email",
"university_id",
"government_username",
"government_email",
"government_id",
"court_username",
"court_email",
"court_id",
"library_username",
"library_email",
"library_id",
"club_username",
"club_email",
"club_id",
"association_username",
"association_email",
"association_id",
"membership_username",
"membership_email",
"membership_id",
"certificate_username",
"certificate_email",
"certificate_id",
"transaction_username",
"transaction_email",
"transaction_id",
"record_username",
"record_email",
"record_id",
"file_username",
"file_email",
"file_id",
"project_username",
"project_email",
"project_id",
"task_username",
"task_email",
"task_id",
"assignment_username",
"assignment_email",
"assignment_id",
"product_username",
"product_email",
"product_id",
"service_id",
"service_code",
"service_name",
"appointment_id",
"appointment_code",
"appointment_date",
"reservation_username",
"reservation_email",
"reservation_id",
"booking_username",
"booking_email",
"booking_id",
"event_username",
"event_email",
"event_id",
"meeting_username",
"meeting_email",
"meeting_id",
"conference_username",
"conference_email",
"conference_id",
"session_username",
"session_email",
"session_id",
"subscription_username",
"subscription_email",
"subscription_id",
"plan_id",
"plan_code",
"plan_name",
"product_category",
"product_type",
"service_category",
"service_type",
"subscription_category",
"subscription_type",
"plan_category",
"plan_type",
"transaction_category",
"transaction_type",
"record_category",
"record_type",
"file_category",
"file_type",
"project_category",
"project_type",
"task_category",
"task_type",
"assignment_category",
"assignment_type",
"event_category",
"event_type",
"meeting_category",
"meeting_type",
"conference_category",
"conference_type",
"session_category",
"session_type",
"reservation_category",
"reservation_type",
"booking_category",
"booking_type",
"loyalty_category",
"loyalty_type",
"coupon_category",
"coupon_type",
"gift_card_category",
"gift_card_type",
"reward_category",
"reward_type",
"membership_category",
"membership_type",
"gift_certificate_category",
"gift_certificate_type",
"invoice_category",
"invoice_type",
"shipment_category",
"shipment_type",
"payment_category",
"payment_type",
"purchase_category",
"purchase_type",
"order_category",
"order_type",
"account_type",
"customer_type",
"client_type",
"user_type",
"member_type",
"employee_type",
"partner_type",
"vendor_type",
"supplier_type",
"contractor_type",
"subscriber_type",
"patient_type",
"student_type",
"organization_type",
"school_type",
"university_type",
"government_type",
"court_type",
"library_type",
"club_type",
"association_type",
"membership_type",
"certificate_type",
"transaction_type",
"record_type",
"file_type",
"project_type",
"task_type",
"assignment_type",
"product_type",
"service_type",
"appointment_type",
"reservation_type",
"booking_type",
"event_type",
"meeting_type",
"conference_type",
"session_type",
"subscription_type",
"plan_type",
"product_brand",
"product_model",
"product_variant",
"service_brand",
"service_model",
"service_variant",
"plan_brand",
"plan_model",
"plan_variant",
"appointment_location",
"reservation_location",
"booking_location",
"event_location",
"meeting_location",
"conference_location",
"session_location",
"subscription_location",
"product_location",
"service_location",
"plan_location",
"transaction_location",
"record_location",
"file_location",
"project_location",
"task_location",
"assignment_location",
"coupon_location",
"discount_location",
"promo_location",
"gift_card_location",
"loyalty_location",
"reward_location",
"membership_location",
"certificate_location",
"invoice_location",
"shipment_location",
"payment_location",
"purchase_location",
"order_location",
"account_location",
"customer_location",
"client_location",
"user_location",
"member_location",
"employee_location",
"partner_location",
"vendor_location",
"supplier_location",
"contractor_location",
"subscriber_location",
"patient_location",
"student_location",
"organization_location",
"school_location",
"university_location",
"government_location",
"court_location",
"library_location",
"club_location",
"association_location",
"membership_location",
"certificate_location",
"transaction_location",
"record_location",
"file_location",
"project_location",
"task_location",
"assignment_location",
"coupon_location",
"discount_location",
"promo_location",
"gift_card_location",
"loyalty_location",
"reward_location",
"membership_location",
"certificate_location",
"invoice_location",
"shipment_location",
"payment_location",
"purchase_location",
"order_location",
"account_location",
"customer_location",
"client_location",
"user_location",
"member_location",
"employee_location",
"partner_location",
"vendor_location",
"supplier_location",
"contractor_location",
"subscriber_location",
"patient_location",
"student_location",
"organization_location",
"school_location",
"university_location",
"government_location",
"court_location",
"library_location",
"club_location",
"association_location",
"membership_location",
"certificate_location",
"transaction_location",
"record_location",
"file_location",
"project_location",
"task_location",
"assignment_location",
"coupon_location",
"discount_location",
"promo_location",
"gift_card_location",
"loyalty_location",
"reward_location",
"membership_location",
"certificate_location",
"invoice_location",
"shipment_location",
"payment_location",
"purchase_location",
"order_location",
"account_location",
"customer_location",
"client_location",
"user_location",
"member_location",
"employee_location",
"partner_location",
"vendor_location", "social_media_username",
"social_media_id",
"social_media_profile",
"avatar_url",
"bio",
"interests",
"preferences",
"likes",
"dislikes",
"comments",
"reviews",
"ratings",
"purchase_history",
"search_history",
"browsing_history",
"cookies",
"device_id",
"device_type",
"browser_type",
"operating_system",
"geolocation",
"payment_method",
"transaction_history",
"subscription_history",
"login_history",
"activity_log",
"session_token",
"authentication_token",
"access_token",
"refresh_token",
"api_key",
"security_question",
"security_answer",
"security_code",
"two_factor_authentication",
"account_recovery_email",
"account_recovery_phone",
"notification_preferences",
"email_notification",
"sms_notification",
"push_notification",
"marketing_opt_in",
"newsletter_opt_in",
"communication_preferences",
"privacy_settings",
"account_status",
"membership_status",
"subscription_status",
"order_status",
"payment_status",
"shipping_status",
"transaction_status",
"booking_status",
"event_status",
"meeting_status",
"conference_status",
"session_status",
"plan_status",
"appointment_status",
"reservation_status",
"loyalty_status",
"reward_status",
"service_status",
"product_status",
"file_status",
"project_status",
"task_status",
"assignment_status",
"record_status",
"coupon_status",
"discount_status",
"promo_status",
"gift_card_status",
"account_creation_date",
"last_login_date",
"last_activity_date",
"last_purchase_date",
"last_order_date",
"last_payment_date",
"last_shipment_date",
"last_transaction_date",
"last_booking_date",
"last_event_date",
"last_meeting_date",
"last_conference_date",
"last_session_date",
"last_plan_date",
"last_appointment_date",
"last_reservation_date",
"last_loyalty_activity_date",
"last_reward_activity_date",
"last_service_date",
"last_product_date",
"last_file_date",
"last_project_date",
"last_task_date",
"last_assignment_date",
"last_record_date",
"last_coupon_date",
"last_discount_date",
"last_promo_date",
"last_gift_card_date",
"last_notification_date",
"terms_and_conditions_accepted",
"privacy_policy_accepted",
"cookie_policy_accepted",
"marketing_consent_accepted",
"age_verification",
"content_preferences",
"subscription_preferences",
"purchase_preferences",
"account_preferences",
"notification_sound",
"notification_frequency",
"notification_sound_volume",
"dark_mode_preference",
"language_preference",
"currency_preference",
"timezone_preference",
"billing_address",
"shipping_address",
"billing_contact",
"shipping_contact",
"billing_method",
"shipping_method",
"billing_details",
"shipping_details",
"billing_information",
"shipping_information",
"billing_notes",
"shipping_notes",
"billing_instructions",
"shipping_instructions",
"return_policy",
"refund_policy",
"exchange_policy",
"support_contact",
"customer_support_hours",
"help_center",
"FAQ",
"customer_reviews",
"customer_testimonials",
"customer_feedback",
"customer_service_rating",
"customer_satisfaction_survey",
"customer_complaints",
"customer_support_ticket",
"customer_support_request",
"customer_support_chat",
"customer_support_email",
"customer_support_phone",
"customer_support_social_media",
"product_description",
"service_description",
"plan_description",
"event_description",
"meeting_description",
"conference_description",
"session_description",
"appointment_description",
"reservation_description",
"loyalty_program_description",
"reward_description",
"file_description",
"project_description",
"task_description",
"assignment_description",
"record_description",
"coupon_description",
"discount_description",
"promo_description",
"gift_card_description",
"organization_description",
"school_description",
"university_description",
"government_description",
"court_description",
"library_description",
"club_description",
"association_description",
"membership_description",
"certificate_description",
"transaction_description",
"security_and_privacy_policy",
"data_retention_policy",
"data_security_measures",
"data_breach_notification",
"compliance_certifications",
"third_party_data_sharing",
"cookies_policy",
"tracking_technologies",
"website_terms_of_service",
"website_acceptable_use_policy",
"website_disclaimer",
"website_accessibility_policy",
"website_community_guidelines",
"website_user_agreement",
"website_user_content_policy",
"website_dmca_policy",
"website_copyright_policy",
"website_trademark_policy",
"website_content_license",
"website_feedback_policy",
"website_modification_policy",
"website_authentication_policy",
"website_login_security",
"website_account_security",
"website_transaction_security",
"website_data_encryption",
"website_firewall",
"website_antivirus",
"website_secure_socket_layer",
"website_two_factor_authentication",
"website_account_lockout_policy",
"website_password_policy",
"website_session_timeout_policy",
"website_account_recovery_policy",
"website_privacy_settings",
"website_data_access_request",
"website_data_portability_request",
"website_data_deletion_request",
"website_data_rectification_request",
"website_data_security_request",
"website_data_breach_response",
"website_data_protection_officer_contact",
"website_terms_and_conditions_update_notification",
"website_privacy_policy_update_notification",
"website_cookie_policy_update_notification",
"website_security_update_notification",
"website_user_agreement_update_notification",
"website_dmca_policy_update_notification",
"website_content_license_update_notification",
"website_feedback_policy_update_notification",
"website_modification_policy_update_notification",
"website_authentication_policy_update_notification",
"website_login_security_update_notification",
"website_account_security_update_notification",
"website_transaction_security_update_notification",
"website_data_encryption_update_notification",
"website_firewall_update_notification",
"website_antivirus_update_notification",
"website_secure_socket_layer_update_notification",
"website_two_factor_authentication_update_notification",
"website_account_lockout_policy_update_notification",
"website_password_policy_update_notification",
"website_session_timeout_policy_update_notification",
"website_account_recovery_policy_update_notification",
"website_privacy_settings_update_notification",
"website_data_breach_response_update_notification",
"website_data_protection_officer_contact_update_notification",
"feedback_survey",
"customer_satisfaction_score",
"net_promoter_score",
"website_traffic_analytics",
"conversion_rate",
"average_order_value",
"cart_abandonment_rate",
"customer_retention_rate",
"customer_lifetime_value",
"visitor_demographics",
"visitor_behavior",
"website_performance_metrics",
"customer_acquisition_cost",
"return_on_investment",
"customer_feedback_analysis",
"market_trends_analysis",
"competitor_analysis",
"social_media_engagement",
"social_media_mentions",
"social_media_shares",
"social_media_likes",
"social_media_followers",
"social_media_influence_score",
"social_media_trends",
"brand_reputation_management",
"brand_mentions",
"brand_sentiment",
"brand_recognition",
"brand_image",
"brand_crisis_management",
"marketing_campaign_metrics",
"email_campaign_metrics",
"social_media_campaign_metrics",
"paid_advertising_metrics",
"search_engine_optimization_metrics",
"content_marketing_metrics",
"affiliate_marketing_metrics",
"customer_acquisition_metrics",
"customer_retention_metrics",
"product_sales_metrics",
"service_performance_metrics",
"plan_subscription_metrics",
"event_attendance_metrics",
"meeting_participation_metrics",
"conference_engagement_metrics",
"loyalty_program_engagement_metrics",
"reward_redemption_metrics", "device_id",
"advertising_id",
"cookie_id",
"user_id",
"session_id",
"tracking_pixel",
"IP_address",
"browser_fingerprint",
"MAC_address",
"IMEI_number",
"SIM_card_serial_number",
"GPS_coordinates",
"WiFi_SSID",
"Bluetooth_MAC_address",
"RFID_tags",
"NFC_tags",
"social_media_handle",
"hashed_email",
"hashed_phone_number",
"hashed_user_id",
"hashed_custom_identifier", "device_type",
"operating_system",
"browser_type",
"screen_resolution",
"viewport_size",
"language",
"timezone",
"referrer",
"utm_parameters",
"conversion_event",
"click_through_rate",
"engagement_rate",
"interaction_event",
"mouse_clicks",
"keyboard_input",
"scrolling_behavior",
"time_spent_on_page",
"geo_location",
"country",
"region",
"city",
"zip_code",
"ISP",
"connection_speed",
"age",
"gender",
"interests",
"online_behavior",
"purchase_history",
"search_history",
"social_media_activity",
"email",
"phone_number",
"address",
"username",
"account_ID",
"loyalty_card_number",
"transaction_ID",
"product_ID",
"service_ID",
"plan_ID",
"event_ID",
"membership_ID",
"certificate_ID",
"file_ID",
"project_ID",
"task_ID",
"assignment_ID",
"record_ID",
"coupon_ID",
"discount_ID",
"promo_ID",
"gift_card_ID",
"organization_ID",
"school_ID",
"university_ID",
"government_ID",
"court_ID",
"library_ID",
"club_ID",
"association_ID",
"customer_ID",
"client_ID",
"user_ID",
"member_ID",
"employee_ID",
"partner_ID",
"vendor_ID",
"supplier_ID",
"contractor_ID",
"subscriber_ID",
"patient_ID",
"student_ID",
"visit_ID",
"clickstream_ID",
"session_recordings_ID",
"event_tracking_ID",
"error_tracking_ID",
"surveys_responses_ID",
"exit_surveys_ID",
"pop-up_engagement_ID",
"chatbot_interactions_ID",
"social_shares_ID",
"video_views_ID",
"audio_listens_ID",
"download_events_ID",
"external_link_clicks_ID",
"file_upload_events_ID",
"ad_impressions_ID",
"ad_clicks_ID",
"ad_conversion_ID",
"affiliate_impressions_ID",
"affiliate_clicks_ID",
"affiliate_conversions_ID",
"search_engine_impressions_ID",
"search_engine_clicks_ID",
"search_engine_conversions_ID",
"hashed_email_ID",
"hashed_phone_number_ID",
"hashed_user_id_ID",
"hashed_custom_identifier_ID", "social_security_number"
"passport_number"
"driver_license_number"
"national_ID_number"
"bank_account_number"
"credit_card_number"
"debit_card_number"
"insurance_policy_number"
"healthcare_ID_number"
"tax_ID_number"
"employee_ID_number"
"student_ID_number"
"voter_registration_number"
"vehicle_registration_number"
"license_plate_number"
"library_card_number"
"employee_badge_number"
"membership_card_number"
"customer_account_number"
"client_account_number"
"patient_ID_number"
"subscriber_ID_number"
"transaction_reference_number"
"order_number"
"invoice_number"
"purchase_order_number"
"tracking_code"
"shipment_tracking_number"
"reservation_number"
"booking_reference_number"
"event_ticket_number"
"meeting_ID_number"
"conference_ID_number"
"session_ID_number"
"subscription_ID_number"
"plan_ID_number"
"loyalty_card_member_ID"
"coupon_code"
"discount_code"
"promo_code"
"gift_card_code"
"reward_points_balance"
"username"
"email_address"
"phone_number"
"physical_address"
"shipping_address"
"billing_address"
"biometric_data"
"fingerprints"
"retina_scan"
"voice_print"
"handwriting_sample"
"signature"
"DNA_sequence"
"facial_recognition_data"
"iris_scan"
"blood_type", "town"]

found_terms = set()

# Perform search for each URL
for url in urls_to_check:
    search_and_save(url, search_keywords, found_terms)

# Output file
output_file_path = "found_terms.txt"

# Write unique terms to the output file
with open(output_file_path, 'w') as file:
    for term in found_terms:
        file.write(f"{term}\n")

print("Search completed for all links. Unique terms saved to found_terms.txt.")