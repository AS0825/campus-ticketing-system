 
### Full Stack Event Ticketing & Seat Management Platform
EventSphere is a full-stack campus event ticketing system designed to automate event registrations, seat allocation, and ticket generation using QR codes.
This project demonstrates frontend-backend integration, REST APIs, database management, and containerization using Docker.

### User Features
- Browse and select events
- Real-time seat selection
- Disabled already-booked seats
- Student registration form
- Booking confirmation preview
- QR code ticket generation
- Payment page simulation

### Admin Features
- Add new events
- View student registrations
- Manage seat allocations
- Dashboard with structured UI

## Tech Stack
**Frontend**
- HTML5
- CSS3 (Modern UI, Gradients, Blur Effects)
- JavaScript (Dynamic Seat Logic)

**Backend**
- Python
- Flask (REST API)

**Database**
- MySQL

**Containerization**
- Docker
- Docker Compose

## System Architecture

Frontend (HTML/CSS/JS)
        ↓
Flask Backend (REST API)
        ↓
MySQL Database
        ↓
Docker Containers (Isolated Deployment)

## 🔄 Booking Workflow
1. User selects event
2. Seat availability is fetched from backend
3. User selects seat
4. Confirmation preview with QR code
5. Payment page redirection
6. Booking stored in database
7. Seat becomes unavailable

## 📦 How to Run (Docker)
```bash
docker compose up --build
