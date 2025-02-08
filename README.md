# PIMKA - Pusat Informasi dan Manajemen Kegiatan Automation Engineering

![Project Status](https://img.shields.io/badge/status-completed-brightgreen) [![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

This project is a case study for the **NoSQL Database** course, implemented using **Python 3.12.3**, the **Flask** framework, and **MongoDB** as the database.

## Technologies Used
- **Python 3.12.3**: Backend logic and API development.
- **Flask**: Web framework for handling HTTP requests.
- **MongoDB**: NoSQL database for storing information.
- **HTML, CSS, JavaScript**: Frontend technologies for UI development.
- **Bootstrap 5**: Responsive design and UI components.

## Features
- **User Authentication**: Login and registration system.
- **Profile Management**: Users can update their profile information.
- **Activity and Consultation Management**: Schedule and manage various activities and consultations.
- **CRUD Operations**:
  - **Users**
  - **Kelas**
  - **Program Studi**
  - **Shift**
  - **Jadwal Apel**
  - **Pengumuman**
  - **Laporan dan Saran**
- **User-Friendly Interface**: Clean and responsive UI for easy navigation.

## Demo

### Landing Page
<img src="https://github.com/user-attachments/assets/4c27ffdc-f858-4984-9886-cfa7bc5665b9" alt="Landing Page Screenshot" width="600">
<img src="https://github.com/user-attachments/assets/219f2f04-5c2b-4b2a-bfad-6814752c7ad0" alt="Additional Screenshots" width="600">
<img src="https://github.com/user-attachments/assets/ba957f7c-300a-479e-b09a-663e8dd8a395" alt="Another Screenshot" width="600">

### Login/Register
<img src="https://github.com/user-attachments/assets/b4d61551-262f-49ac-808c-ab5100fbe56f" alt="Login Screenshot" width="600">
<img src="https://github.com/user-attachments/assets/206d3f92-1375-477d-a4b9-bab346a048f1" alt="Register Screenshot" width="600">

### Admin Panel
#### Edit Profile
<img src="https://github.com/user-attachments/assets/79f57fe6-8079-4b5f-a0c1-8170a94574d6" alt="Edit Profile Screenshot" width="600">

#### CRUD User
<img src="https://github.com/user-attachments/assets/3298d554-567e-4932-b550-289245a27efc" alt="CRUD User Screenshot" width="600">

#### CRUD Kelas
<img src="https://github.com/user-attachments/assets/7c50edb1-f860-47a8-9245-da5828bd64ee" alt="CRUD Kelas Screenshot" width="600">

#### CRUD Program Studi
<img src="https://github.com/user-attachments/assets/ab8b48ba-239e-41c8-ac02-de560be8c46b" alt="CRUD Program Studi Screenshot" width="600">

#### CRUD Shift
<img src="https://github.com/user-attachments/assets/a3bf01b7-d331-4465-8dd9-159b43f79c24" alt="CRUD Shift Screenshot" width="600">

#### CRUD Jadwal Apel
<img src="https://github.com/user-attachments/assets/dd8ea26f-2f8e-4774-bfd2-bb359da1af3d" alt="CRUD Jadwal Apel Screenshot" width="600">

#### CRUD Pengumuman
<img src="https://github.com/user-attachments/assets/3b25962f-2f24-4001-ab85-178fa269a810" alt="CRUD Pengumuman Screenshot" width="600">

#### CRUD Laporan dan Saran
<img src="https://github.com/user-attachments/assets/43be2451-64c2-4af3-8ef9-81bb5c3f2cd2" alt="CRUD Laporan dan Saran Screenshot" width="600">

### User Panel
#### Edit Profile
<img src="https://github.com/user-attachments/assets/37c10fe1-f4cf-4f14-9042-98e79c66e3ca" alt="User Edit Profile Screenshot" width="600">

#### Shift and Jadwal Apel
<img src="https://github.com/user-attachments/assets/4360a60b-0323-4e8d-9e07-7df9dd620feb" alt="User Shift Screenshot" width="600">

#### Pengumuman
<img src="https://github.com/user-attachments/assets/97f47d19-e15d-4bcb-8f08-28cec6ac7d06" alt="User Pengumuman Screenshot" width="600">

## Setup

1. **Install Python 3.12.3**  
   Download Python from the [official Python website](https://www.python.org/).

2. **Clone the Repository**  
   Open your terminal and execute:
   ```bash
   git clone <repository_url>
   cd PIMKA
   ```

3. **Set up a virtual environment and activate it:**
   ```bash
   python -m venv env
   cd env/Scripts
   activate
   cd ../..
   ```

4. **Install the required Python packages:**
   ```bash
   pip install flask pymongo
   ```

5. **Run the application:**
   ```bash
   py app.py
   ```

   Now, you should be able to access the application at `localhost:5000`.

## Project Status
This project is **completed** and will not be further developed.

## Contributions
Feel free to submit issues or contribute by creating pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
