describe('Reports', () => {
  beforeEach(() => {
    cy.login('testuser', 'password123')
    cy.visit('/reports')
  })

  it('should display reports page', () => {
    cy.contains('Daily Reports').should('be.visible')
  })

  it('should show empty state when no reports exist', () => {
    cy.contains('No reports available').should('be.visible')
  })

  it('should display report cards when reports exist', () => {
    // This test assumes there are reports in the system
    // In a real scenario, you might need to create meals first
    cy.get('.report-card').should('exist')
  })
})

