/// <reference types="cypress" />

// sample.spec.js created with Cypress
//
// Start writing your Cypress tests below!
// If you're unfamiliar with how Cypress works,
// check out the link below and learn how to write your first test:
// https://on.cypress.io/writing-first-test
import { faker } from "@faker-js/faker";

describe('NavBar', () => {

  it('Landing Page', () => {
    cy.visit("http://localhost").viewport(1600, 900);
  });
  it('Space Event', () => {
    cy.get("#nav-space-events").click();
  });
  it('About Us', () => {
    cy.get("#nav-about-us").click();
  });

  it('Log In', () => {
    cy.get("#nav-log-in").click();
    cy.get("#log-in-email").type("admin@gmail.com");
    cy.get("#log-in-password").type("admin123");

    cy.get("#log-in-btn").click();
  });

  it('Space List', () => {
    cy.get("#nav-space-list").click();
  });
  it('Owner List', () => {
    cy.get("#nav-owner-list").click();
  });
  it('Log In Page', () => {
    cy.get("#nav-log-out").click();
  });
});

