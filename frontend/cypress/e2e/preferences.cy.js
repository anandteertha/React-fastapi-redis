describe('Preferences', () => {
  beforeEach(() => {
    cy.login('testuser', 'password123')
    cy.visit('/preferences')
  })

  it('should display preferences form', () => {
    cy.contains('Preferences').should('be.visible')
    cy.contains('Daily Targets').should('be.visible')
  })

  it('should allow setting target calories', () => {
    cy.get('input[placeholder*="2000"]').type('2000')
    cy.get('input[placeholder*="2000"]').should('have.value', '2000')
  })

  it('should allow adding dietary restrictions', () => {
    cy.get('input[placeholder*="vegetarian"]').type('vegetarian')
    cy.get('button').contains('Add').click()
    cy.contains('vegetarian').should('be.visible')
  })
})

