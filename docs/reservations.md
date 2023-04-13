# Reservation of Rooms and Equipment 
## Overview
The Reservation page allows students and organizations to reserve equipment and rooms in the CSXL. This feature ensures that there is a fair system for sharing equipment in the CSXL, and it ensures that there are no overlapping reservations. 

The Reservation page has three tabs: 
* **Reserve**: See equipment and room availability on a given day, and create reservations.
* **My Reservations**: See your upcoming reservations and delete your upcoming reservaitons. 
* **Edit Reservables** (Admin Only) : Add new equipment or delete existing equipment from the CSXL.

## Implementation Notes

Description of database/entity-level representation of your feature
Interesting design choices your team made (we choose to do X over Y, because…)


## Development Concerns
If a new developer wanted to start working on your feature, what kind of guidance or overview would you give them to get them started?
**Relevant Files**:
- backend/
    -   api/
        -   reservable.py: Endpoint definitions relating to Reservables
        -   reservation.py: Endpoint definitions relating to Reservations
    -   entities/
        -   reservable_entity.py: Defines Reservable entity
        -   reservation_entity.py: Defines Reservation entity
    -   models/
        -   reservable.py: 
        -   reservation.py:
    -   script/
        -   create_database.py: Creates all databases
        -   reset_database.py: Clears all databases and reloads them with dev data
        -   dev_data/
            -   reservables.py: Creates Reservable models for development and testing purposes
            -   reservations.py:  Creates Reservation models for development and testing purposes
    -   test/
        -   services/
            -   reservable_test.py
            -   reservation_test.py
    
- frontend/
    -   reservation/
        -   reservation.component.ts: Defines the properties and functionality of Reservation page
        -   reservation.component.spec.ts: Auto-generated unit tests for Reservation component
        -   reservation.component.html: Structures and formats the Reservation page
        -   reservation.component.css: Styling for the Reservation page
        -   reservation.service.ts: Methods for accessing Reservation API calls
        -   reservation.component.spec.ts: Auto-generated unit tests for Reservation component
**Getting Started**: Is there anything special they would need to do to get started?
## Future Work
What directions could this feature be taken in? Given more time, what would you hope was added or improved next?