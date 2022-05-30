/// <reference types="cypress" />
//allows program autocompletion according to cypress library

import { faker } from "@faker-js/faker";

describe("User Menu", () => {
    var i = 0;
    var j = 0;

    //randomised record count

    const imax = 3;
//    const jmax = 5;
    for (i = 0; i < imax; i++) {
        it("Visit LogIn Page", () => { //as starting point of a logged in User
            cy.visit("http://localhost").viewport(1600, 900);
            cy.contains("Email"); //field tags to look for
            cy.contains("Password"); //before test starts

            cy.wait(3000)
            cy.get("#user-menu-button").click();
        })
        it("Visit Space List", () => {//visits Space List
            cy.contains("Space List").click(),
                cy.wait(3000)
        })
        it("Visit Owner List", () => {//visits Owner List
            cy.contains("Owner List").click(),
                cy.wait(3000)
        })
        it("Visit Library", () => {//visits Library
            cy.contains("Library").click(),
                cy.wait(3000)
        })
        it("Visit Account Details", () => {//visits Library
            cy.contains("Account").click(),
                cy.wait(3000)
        })
        it("Logout User", () => {//visits Library
            cy.contains("Logout").click(),
                cy.wait(3000)
        })
    }
})