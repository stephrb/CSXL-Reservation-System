# Reservation of Rooms and Equipment 
## Overview
The Reservation page allows students and organizations to reserve equipment and rooms in the CSXL. This feature ensures that there is a fair system for sharing equipment in the CSXL, and it ensures that there are no overlapping reservations. 

The Reservation page has three tabs: 
* **Reserve:** See equipment and room availability on a given day, and create reservations.
* **My Reservations:**: See your upcoming reservations and delete your upcoming reservaitons. 
* **Edit Reservables** (Admin Only)**:** View, add, and delete existing equipment or rooms from the Reservations page.

**Accessing Reservations Feature:**
View the deployed site at [team-f4-comp423-23s.apps.cloudapps.unc.edu](https://team-f4-comp423-23s.apps.cloudapps.unc.edu). Once at the site, register or sign in, since only registered users can access our feature. If attempting to view the admin features, be sure to sign in with an admin account. Then, click "Reservations" on the sidebar to navigate to the Reservations page.  

## Implementation Notes
Description of database/entity-level representation of your feature
Interesting design choices your team made (we choose to do X over Y, because…)

## Development Concerns
**Relevant Files:**
- backend/
    -   api/
        -   reservable.py: Defines the API endpoints relating to Reservables
        -   reservation.py: Defines the API endpoints relating to Reservations
    -   entities/
        -   reservable_entity.py: Defines Reservable entity stored in database
        -   reservation_entity.py: Defines Reservation entity stored in database
    -   models/
        -   reservable.py: Defines Reservable model used by backend 
        -   reservation.py: Defines Reservation model used by backend
    -   script/
        -   create_database.py: Creates all databases used by the application
        -   reset_database.py: Clears all databases and reloads them with dev data
        -   dev_data/
            -   reservables.py: Creates Reservable models for development and testing purposes
            -   reservations.py:  Creates Reservation models for development and testing purposes
    -   services/
        -   reservable.py: Holds methods that query the database and perform CRUD operations on Reservables
        -   reseravtion.py: Holds methods that query the database and perform CRUD operations on Reservations
    -   test/
        -   services/
            -   reservable_test.py: Unit tests for the reservable service
            -   reservation_test.py: Unit tests for the reservation service
    
- frontend/
    -   reservation/
        -   reservation.component.ts: Defines the properties and functionality of Reservation page
        -   reservation.component.spec.ts: Auto-generated unit tests for Reservation component
        -   reservation.component.html: Structures and formats the Reservation page
        -   reservation.component.css: Styling for the Reservation page
        -   reservation.service.ts: Methods for accessing Reservation API calls
        -   reservation.component.spec.ts: Auto-generated unit tests for Reservation component

**Creating Databases:** 
To create the databases needed for this feature, run the create_database script by running `python3 -m backend.script.create_database` in the terminal. 

**Creating Test Data:** 
Prior to starting the application, run the reset_database script by running `python3 -m backend.script.reset_database` in the terminal. 

**Running App Locally:**
To build and run the app locally, run `honcho start` in the terminal. 

**Accessing Test Docs:**
Once the application is running, navigate to [localhost:1560/docs](http://localhost:1560/docs) in the browser to test endpoints and view endpoint definitions.

**Accessing App Locally:**
Once the application is running, navigate to [localhost:1560/](http://localhost:1560/) in the browser to view the site. To access the site authenticated as Arden Ambassador, use this url: [localhost:1560/auth/as/arden/100000001](http://localhost:1560/auth/as/arden/100000001). To access the site authenticated as Sol Student, use this url: [localhost:1560/auth/as/sol/100000000](http://localhost:1560/auth/as/sol/100000000).

## Future Work
We hope to improve the Reserve tab to make it easier for students to find the ruipment or rooms they need. We plan on incorporating the Reservable description to this page so students can explore the offerings of the CSXL. We also plan on adding a filter by Reservable type to the availability table so students can limit the output to only the type of equipment they wish to reserve. For example, students could filter by type "Room" to only show room availability and hide computer and VR availability.

As of now, students can make as many reservations as they want and as far in advance as they would like. However, we are worried that students could abuse the Reservations feature by making too many reservations, preventing other students from using the CSXL. We also are worried that students who make reservations far in the future may forget about their reservation and not show up. This prevents students from fully utilizing the resources that the CSXL has to offer, so we plan on limiting students to reserving one to two weeks in the future. Another implementation could be providing club leaders with priority to make reservations for rooms and equipment. We could give clubs priority by allowing them to reserve further in the future than other students or by increasing their number of allowed reservations. 

In the future, we also hope to add more functionality for admins of the CSXL. As mentioned above, we hope to alter the amount of reservations students can make and the length of time in advance that students can make reservations. We hope that admins Currently, all equipment is available 24/7, but in actuality, the CSXL is porbably not open all day. Admins should be able to change the hours in which students can reserve equipment and rooms to match the hours of the CSXL.