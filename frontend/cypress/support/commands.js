// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

Cypress.Commands.add('login', (username, password) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/v1/auth/login',
    body: {
      username: username,
      password: password
    }
  }).then((response) => {
    window.localStorage.setItem('token', response.body.access_token)
  })
})

