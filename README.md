# Jordan Heritage & Tourism Explorer


## Project Overview : 


Tourism plays a vital role in Jordan’s economy and national identity, yet many local and international visitors remain unaware of the country’s full range of historical, cultural, and natural attractions. While world-famous sites such as Petra and Wadi Rum draw global attention, countless other heritage and nature destinations across the Kingdom, from the ancient ruins of Umm Qais to the scenic Ajloun forests, are often overlooked due to limited digital exposure and fragmented information sources. This lack of accessibility hinders local tourism growth and reduces opportunities for communities that depend on it.
To address this, our team developed Jordan Heritage & Tourism Explorer, a web-based platform that provides a centralized digital space for users to explore, share, and review tourist and heritage sites across Jordan. The platform promotes domestic tourism, empowers travelers to discover lesser-known destinations, and helps preserve the country’s cultural and natural heritage through community-driven engagement.


## Project Description :


Jordan Heritage & Tourism Explorer is a full-stack Django web application that enables users to explore and contribute to a dynamic, interactive map showcasing Jordan’s heritage and tourist sites.
Through the platform, users can:


*   **Browse Destinations:** Explore a wide array of heritage and tourism sites categorized by historical, nature, and adventure.
*   **View Detailed Information:** Access comprehensive details, read user reviews, and see ratings for each location.
*   **Contribute New Places:** Easily add new destinations to the platform, enriching the community-driven database.
*   **Manage Submissions & Reviews:** Securely log in to oversee your contributions and reviews.


## The system includes:

*   **User Authentication:** Secure login, registration, and logout capabilities to manage user accounts.
*   **CRUD Functionality for Destinations:** Users can create, read, update, and delete the destinations added by the users of this web platform.
*   **Review System:** Users can submit ratings (1-5 stars) and comments for each destination, enhancing community engagement.
*   **Responsive Front-End:** Built with HTML/CSS/JS to ensure a seamless and intuitive user experience across all devices.



## Tech Stack :
*   **Frontend:** HTML5, CSS3, JavaScript
*   **Backend:** Python (Django Framework)
*   **Database:** SQLite3 
*   **Version Control:** Git & GitHub
*   **Tools & IDEs:** Visual Studio Code and  Git Bash 
*   **Other Libraries / Packages:** Pillow (for image handling)


## ERD Diagram : 


![ERDDD](https://github.com/user-attachments/assets/e8b7629a-1cbb-438b-b640-290132109e82)




## Installation Guide : 
These steps are essential for setting up and running your Django project on your local machine. Each step builds on the previous one to ensure a clean and organized work environment.

Follow these steps to set up and run the project locally:

### 1- Clone the repository

Open your terminal and execute the following commands to clone the project and navigate into its directory:

```bash
git clone https://github.com/DanyahOdeh/jordan-heritage-and-tourism-explorer.git

cd jordan-heritage-and-tourism-explorer/
```
### 2- Project setup:

The following steps were implemented to setup the project structure:
 ```bash
pip install django #1
django-admin startproject tourismexplorer #2

 ```
### 3- Start app:

After setting the project, we start the main app:

 ```bash
python manage.py startapp main_app
 ```
And for media upload from the users, installing the pillow library is a essential:

```bash
pip install pillow
 ```
### 4- Run database migrations

To apply database changes:

 ```bash
python manage.py makemigrations
python manage.py migrate

 ```
### 5- Creating a superuser:

To create an administrator account to access the admin panel:
 ```bash
python manage.py createsuperuser

 ```
Follow the instructions to enter your username and password:
 ```bash
Username (leave blank to use 'your name'): admin
Email address: admin@example.com
Password: **********
Password (again): **********
Superuser created successfully.

 ```

### 6- Run the development server

To run the project locally:
 ```bash
python manage.py runserver
 ```
Then open the browser and go to: 
 ```bash
http://127.0.0.1:8000/
 ```

##  User Stories:

Our platform is designed to provide the following experiences for its users:

| ID  | User Story                                                                                                       | Description |
| :-- | :-------------------------------------------------------------------------------------------------------------- | :----------- |
| 1   | **As a user, I want to explore a list of heritage and adventure destinations so that I can discover new places of interest.** | Users can browse destinations categorized as Historical, Nature, or Adventure to easily find places they might want to visit. |
| 2   | **As a user, I want to create an account so that I can add new destinations and share details about them.** | Registered users can contribute by adding new heritage or adventure sites and providing relevant information. |
| 3   | **As a user, I want my submitted destinations to go through admin approval so that only verified content appears publicly.** | Each submitted destination is reviewed by the admin before being visible to ensure accuracy and quality. |
| 4   | **As a user, I want to leave reviews and ratings for destinations so that I can share my experiences with others.** | Users can submit a rating (1–5 stars) and write comments for each destination they visit. |
| 5   | **As a user, I want to view all destinations in a responsive and visually clean layout so that I can browse comfortably on any device.** | The platform offers a modern HTML/CSS design that adapts to various screen sizes for optimal user experience. |
| 6   | **As a user, I want to view detailed pages for each destination so that I can learn more about its description, images, and reviews.** | Each destination page includes images, a detailed description, category, region, and user feedback. |
| 7   | **As a registered user, I want to edit or delete my submitted destinations and reviews so that I can manage my own content.** | Users can update or remove destinations they’ve added, as well as delete their own reviews. |
| 8   | **As a user, I want to search for destinations by name so that I can quickly find specific places.** | The search feature filters destinations by name for easier navigation. |
| 9   | **As a registered user, I want to view the status of my submitted destinations so that I can track whether they are approved, declined, or pending.** | The user dashboard displays the current status of each submitted destination. |
| 10  | **As a user, I want to log in and log out securely so that my personal data and contributions remain protected.** | The system provides secure authentication and session management. |
| 11  | **As a user, I want to navigate easily through the website so that I can access Home, Destinations, and my profile quickly.** | A top navigation bar ensures easy access to main sections of the platform. |





### Summary of Challenges Encountered and Solutions Applied

Throughout the development of the Jordan Heritage & Tourism Explorer platform, several technical and design challenges were encountered. Addressing these challenges not only strengthened the overall functionality of the system but also deepened our understanding of full-stack web development using Django.

One of the main challenges was designing a system that is both scalable and user-friendly for a diverse audience, ranging from casual tourists to administrative users. To achieve this, we adopted a modular full-stack architecture using Django, which allowed a clear separation between backend logic and frontend presentation. Django’s built-in authentication and admin panel significantly accelerated development, while the frontend—built with HTML, CSS, JavaScript, and Leaflet.js—ensured a responsive and accessible user experience.

Ensuring data quality and consistency was another important consideration, as the platform relies heavily on user-generated content. To maintain credibility and prevent spam, a review and moderation workflow was implemented. The admin panel allows administrators to approve or reject new destinations, while the community contributes through a rating and review system that promotes accurate and reliable information.

The following table summarizes specific challenges, solutions, and key learnings encountered during the implementation phase:


| **Challenge**                                              | **Solution**                                                                                                      | **Learning Outcome**                                                  |
| :--------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| Users couldn’t upload images for new destinations          | Configured `MEDIA_ROOT` and `MEDIA_URL` in `settings.py`, and updated forms to handle image fields                | Learned how Django manages file uploads and media storage             |
| Filtering destinations by category wasn’t working          | Used Django ORM filtering in views and added category dropdowns in templates                                      | Understood querysets and how to pass data to templates                |
| Reviews weren’t displaying on destination pages            | Added `related_name` in the `Review` model and updated the template to loop over reviews                          | Learned about model relationships and reverse lookups in Django       |
| Responsive layout issues                                   | Applied CSS Flexbox and Grid and refined media queries                                                            | Enhanced frontend responsiveness and design precision                 |
| Admin needed to approve destinations                       | Added an `is_approved` Boolean field in the `Destination` model and filtered views to display only approved items | Implemented an effective moderation workflow                          |
| Users couldn’t edit or delete their own submissions or reviews | Added secure CRUD views and templates with ownership checks                                                       | Gained experience in permission handling and secure user interactions |



