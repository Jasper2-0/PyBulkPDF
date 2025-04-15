# Gemini Python Projects Collaborative Development Workflow**

## **1\. Purpose**

This document outlines the collaborative development process used for ongoing development of python project. It incorporates Test-Driven Development (TDD) as a core principle while acknowledging the need for flexibility based on the task type.

## **2\. Core Principle: Test-Driven Development (TDD)**

For implementing and modifying core application logic (especially within the Service Layer), we strive to adhere to the Red-Green-Refactor cycle:

* **Red:** Write a test (integration or unit) for the desired functionality *first*. This test should initially fail.
* **Green:** Write the *minimum* amount of implementation code required to make the test pass.
* **Refactor:** Improve the implementation code's structure, clarity, or efficiency while ensuring all tests still pass.

## **3\. Key Project Components & Reference Materials**

During development, refer to:

## **4\. General Workflow Steps**

Collaborative sessions often involve these activities, adapting the approach based on the task:

1. **Define Goal, Analyze & Plan:**
    *Specify the task or feature (e.g., "Implement Feature X," "Add unit tests," "Refine E2E script," "Plan i18n support").
    * Consult relevant documentation and existing code.
    * **For significant features:** Perform upfront analysis (e.g., impact assessment) and create/refine implementation plans collaboratively.
2. **Develop Incrementally (Applying TDD where practical):**
    ***For Core Logic (Services):** Aim for TDD (Write Test -> Implement -> Refactor).
    * **For API Layer Changes:** Write/update integration tests before or concurrently with modifying blueprint routes.
    ***For Scaffolding/Scripts (e.g., E2E runner):** May involve generating initial code first, followed by execution, debugging, and iterative refinement based on feedback and results. Testing might follow initial implementation.
    * **For Planning/Documentation:** Collaborative drafting and refinement in the document itself.
3. **Test & Verify:**
    *Run relevant tests (unit, integration) frequently (`pytest`).
    * Execute scripts (like E2E tests) and analyze their output.
    * Verify that the implementation meets the defined goal.
4. **Refactor:**
    *Review newly added/modified code and documentation for clarity, structure, performance, and adherence to guidelines.
    * Refactor as needed, ensuring tests continue to pass.
5. **Review & Iterate:**
    *Collaboratively discuss results, implementation choices, and potential issues.
    * Provide feedback and identify necessary adjustments.
    * Decide on the next step (e.g., another development cycle, addressing a different task, updating documentation).
