"""
Common constants used across schemas
"""

# User Types
VALID_USER_TYPES = [
    "patient", "doctor", "nurse", "staff", "admin", 
    "receptionist", "pharmacist", "lab_technician", "radiologist"
]

# Payment Methods
VALID_PAYMENT_METHODS = [
    "cash", "card", "credit_card", "debit_card", "upi", 
    "net_banking", "cheque", "insurance", "online", "mobile_payment"
]

# Appointment Statuses
VALID_APPOINTMENT_STATUSES = [
    "scheduled", "confirmed", "checked_in", "in_progress",
    "completed", "cancelled", "no_show", "rescheduled"
]

# Billing Statuses
VALID_BILLING_STATUSES = [
    "pending", "partial", "paid", "overdue", "cancelled", "refunded"
]

# Priority Levels
VALID_PRIORITY_LEVELS = ["low", "normal", "high", "urgent", "emergency"]

# Gender Options
VALID_GENDERS = ["male", "female", "other", "prefer_not_to_say"]

# Blood Groups
VALID_BLOOD_GROUPS = [
    "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "unknown"
]

# Document Types
VALID_DOCUMENT_TYPES = [
    "aadhar", "passport", "driving_license", "voter_id", 
    "pan_card", "insurance_card", "other"
]

# Marital Status
VALID_MARITAL_STATUS = [
    "single", "married", "divorced", "widowed", "separated"
]

# Revenue Sources
VALID_REVENUE_SOURCES = [
    "consultations", "procedures", "pharmacy", "lab", "imaging",
    "room_charges", "emergency", "surgery", "miscellaneous", "insurance"
]

# Resources (for permissions)
VALID_RESOURCES = [
    "patients", "appointments", "doctors", "nurses", "staff",
    "billing", "payments", "prescriptions", "lab_tests", "radiology",
    "pharmacy", "inventory", "departments", "wards", "beds",
    "admissions", "discharges", "procedures", "reports", "settings",
    "users", "roles", "permissions", "audit_logs", "notifications"
]

# Actions (for permissions)
VALID_ACTIONS = [
    "create", "read", "update", "delete", "list", 
    "export", "approve", "reject", "view"
]

# Countries
COMMON_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus",
    "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada",
    "Cape Verde", "Central African Republic", "Chad", "Chile", "China",
    "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia",
    "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti",
    "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia",
    "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras",
    "Hungary", "Iceland", "India", "Indonesia", "Iran",
    "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos",
    "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
    "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova",
    "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
    "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway",
    "Oman", "Pakistan", "Palau", "Palestine", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland",
    "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
    "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal",
    "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
    "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan",
    "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland",
    "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan",
    "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga",
    "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States",
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela",
    "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]