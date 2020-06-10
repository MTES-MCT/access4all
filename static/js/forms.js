window.a4aForms = (function () {
  let _config = {
    fieldSelectorPrefix: ".form-row.field-",
    inputNamePrefix: "accessibilite-0-",
  };

  const rules = {
    // transport
    transport_information: {
      dependsOn: ["transport_station_presence"],
      when: true,
      indent: 1,
    },
    // stationnement
    stationnement_pmr: {
      dependsOn: ["stationnement_presence"],
      when: true,
      indent: 1,
    },
    stationnement_ext_pmr: {
      dependsOn: ["stationnement_ext_presence"],
      when: true,
      indent: 1,
    },
    // presence d'un extérieur et cheminement
    cheminement_ext_terrain_accidente: {
      dependsOn: ["cheminement_ext_presence"],
      when: true,
      indent: 1,
    },
    cheminement_ext_plain_pied: {
      dependsOn: ["cheminement_ext_presence"],
      when: true,
      indent: 1,
    },
    cheminement_ext_nombre_marches: {
      dependsOn: ["cheminement_ext_plain_pied"],
      when: false,
      indent: 2,
    },
    cheminement_ext_reperage_marches: {
      dependsOn: ["cheminement_ext_plain_pied"],
      when: false,
      indent: 2,
    },
    cheminement_ext_main_courante: {
      dependsOn: ["cheminement_ext_plain_pied"],
      when: false,
      indent: 2,
    },
    cheminement_ext_rampe: {
      dependsOn: ["cheminement_ext_plain_pied"],
      when: false,
      indent: 2,
    },
    cheminement_ext_ascenseur: {
      dependsOn: ["cheminement_ext_plain_pied"],
      when: false,
      indent: 2,
    },
    cheminement_ext_pente: {
      dependsOn: ["cheminement_ext_presence"],
      when: true,
      indent: 1,
    },
    cheminement_ext_devers: {
      dependsOn: ["cheminement_ext_presence"],
      when: true,
      indent: 1,
    },
    cheminement_ext_bande_guidage: {
      dependsOn: ["cheminement_ext_presence"],
      when: true,
      indent: 1,
    },
    cheminement_ext_retrecissement: {
      dependsOn: ["cheminement_ext_presence"],
      when: true,
      indent: 1,
    },
    // entrée
    entree_vitree_vitrophanie: {
      dependsOn: ["entree_vitree"],
      when: true,
      indent: 1,
    },
    entree_marches: {
      dependsOn: ["entree_plain_pied"],
      when: false,
      indent: 1,
    },
    entree_marches_reperage: {
      dependsOn: ["entree_plain_pied"],
      when: false,
      indent: 1,
    },
    entree_marches_main_courante: {
      dependsOn: ["entree_plain_pied"],
      when: false,
      indent: 1,
    },
    entree_marches_rampe: {
      dependsOn: ["entree_plain_pied"],
      when: false,
      indent: 1,
    },
    entree_ascenseur: {
      dependsOn: ["entree_plain_pied"],
      when: false,
      indent: 1,
    },
    entree_pmr_informations: {
      dependsOn: ["entree_pmr"],
      when: true,
      indent: 1,
    },
    // accueil
    accueil_cheminement_nombre_marches: {
      dependsOn: ["accueil_cheminement_plain_pied"],
      when: false,
      indent: 1,
    },
    accueil_cheminement_reperage_marches: {
      dependsOn: ["accueil_cheminement_plain_pied"],
      when: false,
      indent: 1,
    },
    accueil_cheminement_main_courante: {
      dependsOn: ["accueil_cheminement_plain_pied"],
      when: false,
      indent: 1,
    },
    accueil_cheminement_rampe: {
      dependsOn: ["accueil_cheminement_plain_pied"],
      when: false,
      indent: 1,
    },
    accueil_cheminement_ascenseur: {
      dependsOn: ["accueil_cheminement_plain_pied"],
      when: false,
      indent: 1,
    },
    // sanitaires
    sanitaires_adaptes: {
      dependsOn: ["sanitaires_presence"],
      when: true,
      indent: 1,
    },
  };

  function getFieldInputs(field) {
    const sourceSelector =
      "input[name=" + _config.inputNamePrefix + field + "]";
    return [].slice.call(document.querySelectorAll(sourceSelector));
  }

  function handleClick(field, style) {
    return function () {
      // reinit value for custom boolean radio choices
      const radioNone = field.querySelector("input[type=radio][value='']");
      if (radioNone) {
        radioNone.click();
      }
      // reinit value for textareas
      const textarea = field.querySelector("textarea");
      if (textarea) {
        textarea.value = "";
      }
      // reinit value for number inputs
      const numberInput = field.querySelector("input[type=number]");
      if (numberInput) {
        numberInput.value = "";
      }
      // apply style
      field.style.display = style;
    };
  }

  function condition(when, inputs, target) {
    if (when) {
      inputs[0].addEventListener("click", handleClick(target, "block"));
      inputs[1].addEventListener("click", handleClick(target, "none"));
      inputs[2].addEventListener("click", handleClick(target, "none"));
    } else {
      inputs[0].addEventListener("click", handleClick(target, "none"));
      inputs[1].addEventListener("click", handleClick(target, "block"));
      inputs[2].addEventListener("click", handleClick(target, "none"));
    }
  }

  function getValue(field) {
    const fieldInput = getFieldInputs(field).filter(function (input) {
      return input.checked;
    })[0];
    if (fieldInput.length === 0) {
      throw new Error("Couldn't find source input element for field: " + field);
    }
    return fieldInput.value;
  }

  function run(config = {}) {
    _config = Object.assign({}, _config, config);

    for (let field in rules) {
      const { dependsOn, when, indent } = rules[field];
      const fieldElement = document.querySelector(
        (_config.fieldSelectorPrefix || "") + field
      );
      if (!fieldElement) {
        continue;
      }
      dependsOn.forEach(function (trigger) {
        // events
        const triggerInputs = getFieldInputs(trigger);
        condition(when, triggerInputs, fieldElement);
        // rendering
        const classes = fieldElement.classList;
        if (when && getValue(trigger) !== "True") {
          classes.add("hidden");
        } else if (!when && getValue(trigger) !== "False") {
          classes.add("hidden");
        }
        classes.add("indented" + indent);
      });
    }
  }

  return { run: run };
})();