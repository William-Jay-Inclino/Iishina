/// <reference types="cypress" />
//allows program autocompletion according to cypress library

import { faker } from "@faker-js/faker";

describe("Owner Module", () => {
  let delete_list = []; //will explore on this later

  var i = 0;
  var j = 0;
    
  //randomised record count
  const imax = Math.floor(Math.random() * 1 + 1); //2
  const jmax = Math.floor(Math.random() * 1 + 1); //6

  for (i = 0; i < imax; i++) {
    it("Visit Owner List Page", () => {
      cy.visit("http://localhost/owner").viewport(1600, 900);

      cy.contains("Owner List"); //button parameters it will look before Automation starts
    });
      
    for (j = 0; j < jmax; j++) {
      it("Add New Owner", () => {
        cy.visit("http://localhost/owner").viewport(1600, 900);
        cy.get("#add-owner-button").click();
                  
        //initializing test variables
        const first_name = faker.name.firstName();
        cy.get("#first-name-input").type(first_name)
      
        const last_name = faker.name.lastName();
        cy.get("#last-name-input").type(last_name)
                  
        const company_name = faker.company.companyName();
        cy.get("#company-name-input").type(company_name)
      
        const space_number = Math.floor(Math.random() * 2) + 1;  //generate random number
        cy.get("#space-amount-select").select(space_number);
      
        const email_address = faker.internet.email();
        cy.get("#email-address-input").type(email_address)
        cy.get("#password-input").type('kitten123') //preset password so random inputs could be reused for login(maybe)
      
        cy.get(".modal-card-title").should('be.visible') //should.be is an assertion function
        cy.get("#submit-owner-button").click();
      });

      // delete owner
      if (j % (jmax + 1) == Math.floor(Math.random() * jmax)) {
        it("Delete owner", () => {
          if (cy.contains("Owner List")) {
            cy.contains("Add Owner");
            cy.get("#edit-button").click();
          }
          else {
            cy.contains("Owner Information");
          }
        
          cy.get("#delete-owner").each((item, ndx) => {
            if (ndx % (imax - 1) == Math.floor(Math.random() * imax)) {
              item.click();
            }
          })
        });
      }

      // update owner
      if (j % (jmax + 1) == Math.floor(Math.random() * jmax)) {
        it("Updates owner", () => {
          cy.reload();
          //if Modal is not visible, cypress should look for these first before Edit Button is clicked
          if (cy.contains("Owner List")) {
            cy.contains("Add Owner");
            cy.get("#edit-button").click();
          }

          else { //assertion to check Modal visibility
            cy.get(".modal-card-title").should('be.visible');
            cy.contains("Owner Information");
            cy.contains("Click to upload"); 
          };

          // generate sensible dummy words
          const edit_first_name = faker.name.firstName();
          const edit_last_name = faker.name.lastName();
          const edit_company_name = faker.company.companyName();
          const edit_space_number = Math.floor(Math.random() * 3) + 1; //generate random number
          const edit_email_address = faker.internet.email().toLocaleLowerCase();
          cy.get("#first-name-input")
            .clear()
            .type(edit_first_name);
      
          cy.get("#last-name-input")
            .clear()
            .type(edit_last_name);
      
          cy.get("#company-name-input")
            .clear()
            .type(edit_company_name);    

          cy.get("#space-amount-select").select(edit_space_number);

          cy.get("#email-address-input")
            .clear()
            .type(edit_email_address);

          //ensures that Cypress is accessing the Modal where the Submit Button is in
          cy.get(".modal-card-title").should('be.visible')

          cy.get("#submit-owner-button").click();
        });
      }      
      }
    }
  }
);
