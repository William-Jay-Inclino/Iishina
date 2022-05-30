/// <reference types="cypress" />

// sample.spec.js created with Cypress
//
// Start writing your Cypress tests below!
// If you're unfamiliar with how Cypress works,
// check out the link below and learn how to write your first test:
// https://on.cypress.io/writing-first-test
import { faker } from "@faker-js/faker";

describe("Layer Module", () => {
  let delete_list = [];

  var i = 0;
  var j = 0;

  // randomize record count
  let imax = Math.floor(Math.random() * 5 + 1);
  let jmax = Math.floor(Math.random() * 10 + 1);

  for (i = 0; i < imax; i++) {
    it("Visits Layer Page", () => {
      cy.visit("http://localhost/layer").viewport(1600, 900);

      cy.contains("Layer List");
      cy.contains("Add Layer");
    });

    // delete some layers
    // j = 0;
    // jmax = 0;

    // if (j % (imax - 1) == Math.floor(Math.random() * imax)) {
    //   it("Delete some layers", () => {
    //     cy.get(".delete-button").each((item, ndx) => {
    //       item.click();
    //       // if (ndx % (imax - 1) == Math.floor(Math.random() * imax) || true) {
    //       //   item.click();
    //       // }
    //     });
    //   });
    // }

    // add some layers
    j = 0;
    jmax = 5;

    for (j = 0; j < jmax; j++) {
      it("Adds new layers", () => {
        cy.contains("Layer List");
        // click some row to set as Current Layer
        cy.get("tr").then(($rows) => {
          if ($rows.length > 1) {
            const r = Math.floor(Math.random() * $rows.length + 1);

            cy.log(r, $rows[r]);
            cy.get("tr").eq(r).click();
          }
        });

        cy.get("#add-layer").click();

        // generate sensible dummy words
        const layer_name =
          faker.word.adjective().toUpperCase() +
          " " +
          faker.word.noun().toUpperCase();

        cy.get("input:last").type(layer_name);
        cy.get("button#submit-button:last").click();
      });
    }

    // update some layers
    // j = 0;
    // jmax = 0;

    // if (j % (imax - 1) == Math.floor(Math.random() * imax)) {
    //   it("Updates some layers", () => {
    //     cy.get(".edit-button").first().click();

    //     // generate sensible dummy words
    //     const layer_name =
    //       faker.word.adjective().toUpperCase() +
    //       " " +
    //       faker.word.noun().toUpperCase();

    //     cy.get("input:last")
    //       .clear()
    //       .type(layer_name + "*");
    //     cy.get("button#submit-button:last").click();
    //   });
    // }
  }
});
