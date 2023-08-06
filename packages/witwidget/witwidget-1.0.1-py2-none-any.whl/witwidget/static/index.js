define(["@jupyter-widgets/base"], function(__WEBPACK_EXTERNAL_MODULE_2__) { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

/* Copyright 2018 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

window.__webpack_public_path__ =
  document.querySelector('body').getAttribute('data-base-url') +
  'nbextensions/wit-widget/';

// Export widget models and views.
module.exports = __webpack_require__(1);


/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

/* Copyright 2018 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

var widgets = __webpack_require__(2);

// What-If Tool View. Renders the tool and provides communication with the
// python backend.
var WITView = widgets.DOMWidgetView.extend({
  render: function() {
    // Load up the WIT polymer element.
    this.loadAndCreateWhatIfToolElement();

    // Add listeners for changes from python.
    this.model.on('change:examples', this.examplesChanged, this);
    this.model.on('change:config', this.configChanged, this);
    this.model.on('change:inferences', this.inferencesChanged, this);
    this.model.on('change:eligible_features',
        this.eligibleFeaturesChanged, this);
    this.model.on('change:mutant_charts', this.mutantChartsChanged, this);
    this.model.on('change:sprite', this.spriteChanged, this);
  },

  /**
   * Loads up the WIT element.
   */
  loadAndCreateWhatIfToolElement: function() {
    const templateLocation =
        window.__webpack_public_path__ + 'wit_jupyter.html';

    // If the vulcanized template is not loaded yet, load it now.
    if (!document.querySelector('link[href="' + templateLocation + '"]')) {
      const link = document.createElement('link');
      link.setAttribute('rel', 'import');
      link.setAttribute('href', templateLocation);

      // Create the polymer element upon loading the template.
      link.onload = () => this.createWhatIfToolElement();

      document.head.appendChild(link);
    } else {
      // If the template is already loaded then create the element.
      this.createWhatIfToolElement();
    }
  },

  /**
   * Creates and configure the WIT polymer element.
   */
  createWhatIfToolElement: function() {
    // Create and attach WIT element to DOM.
    this.view_ = document.createElement(
      'tf-interactive-inference-dashboard');
    this.view_.local = true;
    this.el.appendChild(this.view_);

    // Add listeners for changes from WIT Polymer element. Passes changes
    // along to python.
    this.view_.addEventListener('infer-examples', e => {
      let i = this.model.get('infer') + 1;
      this.model.set('infer', i);
      this.touch();
    });
    this.view_.addEventListener('delete-example', e => {
      this.model.set('delete_example', {'index': e.detail.index});
      this.touch();
    });
    this.view_.addEventListener('duplicate-example', e => {
      this.model.set('duplicate_example', {'index': e.detail.index});
      this.touch();
    });
    this.view_.addEventListener('update-example', e => {
      this.model.set('update_example',
          {'index': e.detail.index, 'example': e.detail.example});
      this.touch();
    });
    this.view_.addEventListener('get-eligible-features', e => {
      let i = this.model.get('get_eligible_features') + 1;
      this.model.set('get_eligible_features', i);
      this.touch();
    });

    this.inferMutantsCounter = 0;
    this.view_.addEventListener('infer-mutants', e => {
      e.detail['infer_mutants_counter'] = this.inferMutantsCounter++;
      this.model.set('infer_mutants', e.detail);
      this.mutantFeature = e.detail.feature_name;
      this.touch();
    });

    // Invoke change listeners for initial settings.
    this.configChanged();
    this.examplesChanged();
    this.spriteChanged();
  },

  // Callback functions for when changes made on python side.
  examplesChanged: function() {
    const examples = this.model.get('examples');
    if (examples && examples.length > 0) {
      this.view_.updateExampleContents(examples, false);
    }
  },
  inferencesChanged: function() {
    const inferences = this.model.get('inferences');
    this.view_.labelVocab = inferences['label_vocab'];
    this.view_.inferences = inferences['inferences'];
  },
  eligibleFeaturesChanged: function() {
    const features = this.model.get('eligible_features');
    this.view_.partialDepPlotEligibleFeatures = features;
  },
  mutantChartsChanged: function() {
    const chartInfo = this.model.get('mutant_charts');
    this.view_.makeChartForFeature(chartInfo.chartType, this.mutantFeature,
        chartInfo.data);
  },
  configChanged: function() {
    const config = this.model.get('config');
    if (config == null) {
      return;
    }
    if ('inference_address' in config) {
      let addresses = config['inference_address'];
      if ('inference_address_2' in config) {
        addresses += ',' + config['inference_address_2'];
      }
      this.view_.inferenceAddress = addresses;
    }
    if ('model_name' in config) {
      let names = config['model_name'];
      if ('model_name_2' in config) {
        names += ',' + config['model_name_2'];
      }
      this.view_.modelName = names;
    }
    if ('model_type' in config) {
      this.view_.modelType = config['model_type'];
    }
    if ('are_sequence_examples' in config) {
      this.view_.sequenceExamples = config['are_sequence_examples'];
    }
    if ('max_classes' in config) {
      this.view_.maxInferenceEntriesPerRun = config['max_classes'];
    }
    if ('multiclass' in config) {
      this.view_.multiClass = config['multiclass'];
    }
    this.view_.updateNumberOfModels();
  },
  spriteChanged: function() {
    const spriteUrl = this.model.get('sprite');
    this.view_.hasSprite = true;
    this.view_.localAtlasUrl = spriteUrl;
    this.view_.updateSprite();
  },
});

module.exports = {
  WITView : WITView
};


/***/ }),
/* 2 */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_2__;

/***/ })
/******/ ])});;
//# sourceMappingURL=index.js.map