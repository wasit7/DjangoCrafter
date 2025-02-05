# **DjangoCrafter**

**DjangoCrafter** is the official repository for the web development course designed to teach students how to create modern, dynamic web applications using Django. This repository serves as a comprehensive resource for mastering backend and frontend integration while leveraging powerful tools like Tailwind CSS, HTMX, and Django REST Framework. 

## **Key Features:**
- **Low-Code Marketplace Prototype:** Build a Craigslist-inspired platform tailored for local communities, such as Pathum Thani.
- **Dynamic Interactions:** Utilize HTMX to create near real-time interactions without full page reloads.
- **Custom UI Design:** Incorporate Tailwind CSS for rapid, responsive, and minimalistic styling.
- **RESTful APIs:** Learn to expose data for external applications using Django REST Framework.
- **Hands-On Labs:** Structured tutorials and exercises for each chapter, enabling practical, incremental learning.
- **Community-Focused Design:** Integrate local elements to reflect the culture and needs of specific communities.

This repository contains:
- Course materials: lecture notes, tutorials, and exercises.
- Source code examples and reusable templates for project development.
- A collaborative platform to foster student creativity and innovation.

**DjangoCrafter** empowers students to craft robust web applications while addressing real-world challenges through modern, efficient development practices. Whether you’re a beginner or an aspiring data scientist, this repository equips you with essential skills to bring your ideas to life.

# Setup
```bash
cp -pr ./_template/ ./week02/
cd week02
docker stop django_project
docker rm django_project
docker-compose up --build
```
