/// <reference types="cypress" />
//allows program autocompletion according to cypress library

import { faker } from "@faker-js/faker";


describe("User Module", () => {
    let delete_list = []; //will explore on this later

    var i = 0;
    var j = 0;

    //randomised record count
    const imax = Math.floor(Math.random() * 1 + 1);
    const jmax = Math.floor(Math.random() * 1 + 1); //will need to tailor this to suit the functionality

    for (i = 0; i < imax; i++) {
        it("Visit Owner List Page", () => {
            cy.visit("http://localhost/owner").viewport(1600, 900);

            cy.contains("User Space"); //button parameters it will look
            cy.contains("Library"); //before Automation starts
            cy.contains("Edit Owner");
        });
            
        j = 0;
        for (j = 0; j < jmax; j++) {
            it("Add Owner", () => {
                cy.get("#addOwner").click();
                cy.wait(1000)

                //initializing test variables
                const first_name = faker.name.firstName();
                cy.get(".inputFirstName").type(first_name)
                cy.wait(1000)

                const last_name = faker.name.lastName();
                cy.get(".inputLastName").type(last_name)
                cy.wait(1000)

                const emailaddress = first_name;
                cy.get(".inputEmailAddress").type(emailaddress + "@email.com")
                cy.get(".inputPassword").type('kitten123')
                cy.wait(2000)

                cy.get(".modal-card-title").should('be.visible') //should be is an assertion function
                cy.get("#submitButtonOwnerForm").click();
            });
        }
    }
});