/// <reference types="cypress" />

// sample.spec.js created with Cypress
//
// Start writing your Cypress tests below!
// If you're unfamiliar with how Cypress works,
// check out the link below and learn how to write your first test:
// https://on.cypress.io/writing-first-test
import { faker } from "@faker-js/faker";

describe('LogIn Page', () => {
  it('Landing Page', () => {

    cy.visit("http://localhost").viewport(1600, 900);

    cy.contains("Log In");
  });

  var j = 0;
  for (j = 0; j < 4; j++) {
    it('Login Failed Attempt', () => {

      const username = faker.internet.email();
      const password = faker.internet.password();

      cy.get("#log-in-email").focus().clear();
      cy.get("#log-in-email").type(username);
      cy.get("#log-in-password").focus().clear();
      cy.get("#log-in-password").type(password);

      cy.get("#log-in-btn").click();
    });
  }

  it('Login Success Attempt', () => {

    cy.get("#log-in-email").focus().clear();
    cy.get("#log-in-email").type("admin@gmail.com");
    cy.get("#log-in-password").focus().clear();
    cy.get("#log-in-password").type("admin123");

    cy.get("#log-in-btn").click();
  });


  it('Logout Attempt', () => {
    cy.get("#nav-log-out").click();
  });
});

