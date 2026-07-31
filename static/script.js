/**
 * CardioPredict AI — client-side form validation
 * ------------------------------------------------
 * Lightweight, dependency-free validation for the patient intake form.
 * Server-side validation in app.py remains the source of truth; this
 * just gives the user immediate, friendly feedback before submission.
 */

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("predict-form");
  if (!form) return;

  const numberFields = form.querySelectorAll('input[type="number"]');
  const radioGroups = getRadioGroupNames(form);

  form.addEventListener("submit", function (event) {
    let firstInvalid = null;
    let isValid = true;

    // Validate numeric fields against their min/max attributes.
    numberFields.forEach(function (field) {
      const errorEl = form.querySelector('[data-error-for="' + field.name + '"]');
      const message = validateNumberField(field);

      if (message) {
        isValid = false;
        field.classList.add("is-invalid");
        if (errorEl) errorEl.textContent = message;
        if (!firstInvalid) firstInvalid = field;
      } else {
        field.classList.remove("is-invalid");
        if (errorEl) errorEl.textContent = "";
      }
    });

    // Validate that every required radio group has a selection.
    radioGroups.forEach(function (name) {
      const checked = form.querySelector('input[name="' + name + '"]:checked');
      const errorEl = form.querySelector('[data-error-for="' + name + '"]');

      if (!checked) {
        isValid = false;
        if (errorEl) errorEl.textContent = "Please select an option.";
        if (!firstInvalid) firstInvalid = form.querySelector('input[name="' + name + '"]');
      } else if (errorEl) {
        errorEl.textContent = "";
      }
    });

    if (!isValid) {
      event.preventDefault();
      if (firstInvalid) {
        firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  });

  // Clear an individual field's error as soon as the user fixes it.
  numberFields.forEach(function (field) {
    field.addEventListener("input", function () {
      const errorEl = form.querySelector('[data-error-for="' + field.name + '"]');
      const message = validateNumberField(field);
      field.classList.toggle("is-invalid", Boolean(message));
      if (errorEl) errorEl.textContent = message || "";
    });
  });

  radioGroups.forEach(function (name) {
    form.querySelectorAll('input[name="' + name + '"]').forEach(function (radio) {
      radio.addEventListener("change", function () {
        const errorEl = form.querySelector('[data-error-for="' + name + '"]');
        if (errorEl) errorEl.textContent = "";
      });
    });
  });

  function validateNumberField(field) {
    if (field.value.trim() === "") {
      return "This field is required.";
    }

    const value = parseFloat(field.value);

    if (Number.isNaN(value)) {
      return "Please enter a valid number.";
    }

    if (value < 0) {
      return "Value cannot be negative.";
    }

    const min = field.hasAttribute("min") ? parseFloat(field.min) : null;
    const max = field.hasAttribute("max") ? parseFloat(field.max) : null;

    if (min !== null && value < min) {
      return "Value must be at least " + min + ".";
    }

    if (max !== null && value > max) {
      return "Value must be no more than " + max + ".";
    }

    return null;
  }

  function getRadioGroupNames(scope) {
    const names = new Set();
    scope.querySelectorAll('input[type="radio"]').forEach(function (radio) {
      names.add(radio.name);
    });
    return Array.from(names);
  }
});
