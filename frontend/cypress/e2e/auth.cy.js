describe('Authentication', () => {
  it('should register a new user', () => {
    cy.visit('/register')
    cy.get('input[type="text"]').first().type('testuser')
    cy.get('input[type="email"]').type('test@example.com')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()
    cy.url().should('include', '/')
  })

  it('should login with valid credentials', () => {
    cy.visit('/login')
    cy.get('input[type="text"]').type('testuser')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()
    cy.url().should('include', '/')
  })

  it('should show error on invalid login', () => {
    cy.visit('/login')
    cy.get('input[type="text"]').type('invaliduser')
    cy.get('input[type="password"]').type('wrongpassword')
    cy.get('button[type="submit"]').click()
    cy.contains('Login failed').should('be.visible')
  })
})

