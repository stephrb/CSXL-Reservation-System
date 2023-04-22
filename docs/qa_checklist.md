# Quality Assurance Checklist
## Backend
- [ ] Ensure appropriate documenation and style according to the Google style guide (https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
  - [ ] Docstrings for every new method and include Args, Returns, and Raises when it is unclear
  - [ ] Docstrings for every class
  - [ ] Punctuation, spelling, grammar, etc
- [ ] Write and run unit tests for all new service level methods, making sure to anticipate edge cases
- [ ] Test API endpoints to ensure desired behavior in /docs
- [ ] Verify permissions are enforced for admin related methods and APIs
- [ ] Implement error handling to provide meaningful and clear error messages to the frontend.
- [ ] Ensure that the API endpoints return appropriate HTTP status codes
- [ ] Verify that the response payloads for API endpoints follow a consistent format
## Frontend
- [ ] Ensure appropriate documentation and style according to the Angular style guide (https://angular.io/guide/styleguide)
  - [ ] Properly comment components and functions.
  - [ ] Use consistent naming conventions for variables, functions, and components.
  - [ ] Follow the Single Responsibility Principle and ensure each component has a clear and distinct purpose.
- [ ] Implement error handling to provide meaningful and clear error messages to the user.
- [ ] Ensure the reservation system integrates well with the existing website layout and design.
- [ ] Verify the UI leads to a clean and accessible user experience
- [ ] Ensure that the system handles unexpected user inputs and errors gracefully
