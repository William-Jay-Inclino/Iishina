/// <reference types="cypress" />
//allows program autocompletion according to cypress library

import { faker } from "@faker-js/faker";

describe("User Menu", () => {
    var i = 0;
    const imax = 2;

    for (i = 0; i < imax; i++) {
        it("Visit LogIn Page", () => {
            cy.visit("http://localhost").viewport(1600, 900);
            cy.contains("Email")
            cy.contains("Password")
        });

        it("Log In User", () => {
            cy.get("#log-in-email").type("caroline.bureros@gmail.com");
            cy.get("#log-in-password").type("@RoKitten123");
            cy.get("#log-in-btn").contains("Log In").click();
        })
        it("Visit Space List", () => {//visits Space List
            cy.get("#user-menu-select").select("1");
        });

        it("Visit Owner List", () => {//visits Owner List
            cy.get("#user-menu-select").select("2");
        });

        it("Visit Library", () => {//visits Library
            cy.get("#user-menu-select").select("3");
        });

        it("Visit Account Details", () => {//visits Account Details
            cy.get("#user-menu-select").select("4");
        });
    
        it("Logout User", () => {//Logout User
            cy.get("#user-menu-select").select("5");
        });
    }
})
