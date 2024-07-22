# Bus-Seat-Reservation

# Bus Reservation System

## Description
This is a web-based bus reservation system designed to allow users to reserve seats on a bus. The system includes user authentication (login and registration), seat selection, and confirmation of reservation details.

## Features
- User Registration
- User Login
- Selection of bus time and place
- Selection of available bus seats with visual representation
- Confirmation of reservation details
- Logout functionality

## Technologies Used
- Flask (Python)
- Jinja2 (for templating)
- HTML, CSS, JavaScript (for frontend)
- SQLite (for the database)

## Project Structure
bus_reservation/
│
├── static/
│ ├── style.css
│ ├── stylehome.css
│ ├── logo.png
│ └── app.js
│
├── templates/
│ ├── base.html
│ ├── home.html
│ ├── login.html
│ ├── register.html
│ ├── choose_time_place.html
│ ├── choose_seat.html
│ └── result.html
│
├── app.py
├── models.py
├── README.txt
└── requirements.txt

## Installation and Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bus_reservation.git
   cd bus_reservation

pip install -r requirements.txt
python models.py
flask run

#Acknowledgements

    Thanks to Flask and Jinja2 for making web development in Python easy and fun.
    Thanks to the community for the resources and tutorials that helped in building this project.

For any inquiries, please contact [soufyane el-asly] at [elasslysoufyane@gmail.com]

