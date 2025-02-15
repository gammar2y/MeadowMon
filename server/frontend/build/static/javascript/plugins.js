// Example of a jQuery plugin for a slider
'use strict';

/**
 * Plugins engine.
 *
 * @module plugins
 *
 * @param {Object} data input data
 * @param {Object} info extra information
 * @param {Object} plugins plugins object from config
 * @return {Object} output data
 */


/**
 * Direct or reverse per-item loop.
 *
 * @param {Object} data input data
 * @param {Object} info extra information
 * @param {Array} plugins plugins list to process
 * @param {Boolean} [reverse] reverse pass?
 * @return {Object} output data
 */
function perItem(data, info, plugins, reverse) {

    function monkeys(items) {

        items.content = items.content.filter(function(item) {

            // reverse pass
            if (reverse && item.content) {
                monkeys(item);
            }

            // main filter
            var filter = true;

            for (var i = 0; filter && i < plugins.length; i++) {
                var plugin = plugins[i];

                if (plugin.active && plugin.fn(item, plugin.params, info) === false) {
                    filter = false;
                }
            }

            // direct pass
            if (!reverse && item.content) {
                monkeys(item);
            }

            return filter;

        });

        return items;

    }

    return monkeys(data);

}

/**
 * "Full" plugins.
 *
 * @param {Object} data input data
 * @param {Object} info extra information
 * @param {Array} plugins plugins list to process
 * @return {Object} output data
 */
function full(data, info, plugins) {

    plugins.forEach(function(plugin) {
        if (plugin.active) {
            data = plugin.fn(data, plugin.params, info);
        }
    });

    return data;

}
(function($) {
    $.fn.simpleSlider = function(options) {
        var settings = $.extend({
            speed: 500,
            pause: 3000,
            transition: 'fade'
        }, options);

        return this.each(function() {
            var $this = $(this);
            var $slides = $this.find('.slides');
            var currentIndex = 0;

            function showNextSlide() {
                $slides.eq(currentIndex).fadeOut(settings.speed);
                currentIndex = (currentIndex + 1) % $slides.length;
                $slides.eq(currentIndex).fadeIn(settings.speed);
            }

            setInterval(showNextSlide, settings.pause);
        });
    };
}(jQuery));

var _pluginJsx = _interopRequireDefault(require("@svgr/plugin-jsx"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const DEFAULT_PLUGINS = [_pluginJsx.default];

function getPlugins(config, state) {
  if (config.plugins) {
    return config.plugins;
  }

  if (state.caller && state.caller.defaultPlugins) {
    return state.caller.defaultPlugins;
  }

  return DEFAULT_PLUGINS;
}

function resolvePlugin(plugin) {
  if (typeof plugin === 'function') {
    return plugin;
  }

  if (typeof plugin === 'string') {
    return loadPlugin(plugin);
  }

  throw new Error(`Invalid plugin "${plugin}"`);
}

const pluginCache = {};

function loadPlugin(moduleName) {
  if (pluginCache[moduleName]) {
    return pluginCache[moduleName];
  }

  try {
    // eslint-disable-next-line
    const plugin = require(moduleName);

    if (!plugin.default || !plugin) {
      throw new Error(`Invalid plugin "${moduleName}"`);
    }

    pluginCache[moduleName] = plugin.default || plugin;
    return pluginCache[moduleName];
  } catch (error) {
    throw new Error(`Module "${moduleName}" missing. Maybe \`npm install ${moduleName}\` could help!`);
  }
}

// Example of a form validation plugin
(function($) {
    $.fn.validateForm = function() {
        return this.each(function() {
            var $form = $(this);
            $form.on('submit', function(event) {
                var isValid = true;
                $form.find('input, textarea').each(function() {
                    if ($(this).val() === '') {
                        isValid = false;
                        $(this).addClass('error');
                    } else {
                        $(this).removeClass('error');
                    }
                });
                if (!isValid) {
                    event.preventDefault();
                }
            });
        });
    };
}(jQuery));

// Initialize plugins
$(document).ready(function() {
    $('.slider').simpleSlider();
    $('form').validateForm();
});

function pluginsFrom(plugins) {
    var flatPlugins = {
      level1Value: [],
      level1Property: [],
      level2Block: []
    };
  
    plugins = plugins || [];
  
    flatPlugins.level1Value = plugins
      .map(function(plugin) { return plugin.level1 && plugin.level1.value; })
      .filter(function(plugin) { return plugin != null; });
  
    flatPlugins.level1Property = plugins
      .map(function(plugin) { return plugin.level1 && plugin.level1.property; })
      .filter(function(plugin) { return plugin != null; });
  
    flatPlugins.level2Block = plugins
      .map(function(plugin) { return plugin.level2 && plugin.level2.block; })
      .filter(function(plugin) { return plugin != null; });
  
    return flatPlugins;
  }

  const req = require('./req.js')

  /**
   * Plugin Loader
   *
   * @private
   * @method load
   *
   * @param  {String} plugin PostCSS Plugin Name
   * @param  {Object} options PostCSS Plugin Options
   *
   * @return {Function} PostCSS Plugin
   */
  const load = (plugin, options, file) => {
    try {
      if (
        options === null ||
        options === undefined ||
        Object.keys(options).length === 0
      ) {
        return req(plugin, file)
      } else {
        return req(plugin, file)(options)
      }
    } catch (err) {
      throw new Error(`Loading PostCSS Plugin failed: ${err.message}\n\n(@${file})`)
    }
  }
  
  /**
   * Load Plugins
   *
   * @private
   * @method plugins
   *
   * @param {Object} config PostCSS Config Plugins
   *
   * @return {Array} plugins PostCSS Plugins
   */
  const plugins = (config, file) => {
    let plugins = []
  
    if (Array.isArray(config.plugins)) {
      plugins = config.plugins.filter(Boolean)
    } else {
      plugins = Object.keys(config.plugins)
        .filter((plugin) => {
          return config.plugins[plugin] !== false ? plugin : ''
        })
        .map((plugin) => {
          return load(plugin, config.plugins[plugin], file)
        })
    }
  
    if (plugins.length && plugins.length > 0) {
      plugins.forEach((plugin, i) => {
        if (plugin.default) {
          plugin = plugin.default
        }
  
        if (plugin.postcss === true) {
          plugin = plugin()
        } else if (plugin.postcss) {
          plugin = plugin.postcss
        }
  
        if (
          // eslint-disable-next-line
          !(
            (typeof plugin === 'object' && Array.isArray(plugin.plugins)) ||
            (typeof plugin === 'object' && plugin.postcssPlugin) ||
            (typeof plugin === 'function')
          )
        ) {
          throw new TypeError(`Invalid PostCSS Plugin found at: plugins[${i}]\n\n(@${file})`)
        }
      })
    }
  
    return plugins
  }
  Object.defineProperty(exports, "__esModule", {
    value: true
  });
  exports.loadPlugin = loadPlugin;
  exports.loadPreset = loadPreset;
  exports.resolvePreset = exports.resolvePlugin = void 0;
  function _debug() {
    const data = require("debug");
    _debug = function () {
      return data;
    };
    return data;
  }
  function _path() {
    const data = require("path");
    _path = function () {
      return data;
    };
    return data;
  }
  var _async = require("../../gensync-utils/async.js");
  var _moduleTypes = require("./module-types.js");
  function _url() {
    const data = require("url");
    _url = function () {
      return data;
    };
    return data;
  }
  var _importMetaResolve = require("../../vendor/import-meta-resolve.js");
  const debug = _debug()("babel:config:loading:files:plugins");
  const EXACT_RE = /^module:/;
  const BABEL_PLUGIN_PREFIX_RE = /^(?!@|module:|[^/]+\/|babel-plugin-)/;
  const BABEL_PRESET_PREFIX_RE = /^(?!@|module:|[^/]+\/|babel-preset-)/;
  const BABEL_PLUGIN_ORG_RE = /^(@babel\/)(?!plugin-|[^/]+\/)/;
  const BABEL_PRESET_ORG_RE = /^(@babel\/)(?!preset-|[^/]+\/)/;
  const OTHER_PLUGIN_ORG_RE = /^(@(?!babel\/)[^/]+\/)(?![^/]*babel-plugin(?:-|\/|$)|[^/]+\/)/;
  const OTHER_PRESET_ORG_RE = /^(@(?!babel\/)[^/]+\/)(?![^/]*babel-preset(?:-|\/|$)|[^/]+\/)/;
  const OTHER_ORG_DEFAULT_RE = /^(@(?!babel$)[^/]+)$/;
  const resolvePreset = exports.resolvePreset = resolveStandardizedName.bind(null, "preset");
  function* loadPlugin(name, dirname) {
    const filepath = resolvePlugin(name, dirname, yield* (0, _async.isAsync)());
    const value = yield* requireModule("plugin", filepath);
    debug("Loaded plugin %o from %o.", name, dirname);
    return {
      filepath,
      value
    };
  }
  function* loadPreset(name, dirname) {
    const filepath = resolvePreset(name, dirname, yield* (0, _async.isAsync)());
    const value = yield* requireModule("preset", filepath);
    debug("Loaded preset %o from %o.", name, dirname);
    return {
      filepath,
      value
    };
  }
  function standardizeName(type, name) {
    if (_path().isAbsolute(name)) return name;
    const isPreset = type === "preset";
    return name.replace(isPreset ? BABEL_PRESET_PREFIX_RE : BABEL_PLUGIN_PREFIX_RE, `babel-${type}-`).replace(isPreset ? BABEL_PRESET_ORG_RE : BABEL_PLUGIN_ORG_RE, `$1${type}-`).replace(isPreset ? OTHER_PRESET_ORG_RE : OTHER_PLUGIN_ORG_RE, `$1babel-${type}-`).replace(OTHER_ORG_DEFAULT_RE, `$1/babel-${type}`).replace(EXACT_RE, "");
  }
  function* resolveAlternativesHelper(type, name) {
    const standardizedName = standardizeName(type, name);
    const {
      error,
      value
    } = yield standardizedName;
    if (!error) return value;
    if (error.code !== "MODULE_NOT_FOUND") throw error;
    if (standardizedName !== name && !(yield name).error) {
      error.message += `\n- If you want to resolve "${name}", use "module:${name}"`;
    }
    if (!(yield standardizeName(type, "@babel/" + name)).error) {
      error.message += `\n- Did you mean "@babel/${name}"?`;
    }
    const oppositeType = type === "preset" ? "plugin" : "preset";
    if (!(yield standardizeName(oppositeType, name)).error) {
      error.message += `\n- Did you accidentally pass a ${oppositeType} as a ${type}?`;
    }
    if (type === "plugin") {
      const transformName = standardizedName.replace("-proposal-", "-transform-");
      if (transformName !== standardizedName && !(yield transformName).error) {
        error.message += `\n- Did you mean "${transformName}"?`;
      }
    }
    error.message += `\n
  Make sure that all the Babel plugins and presets you are using
  are defined as dependencies or devDependencies in your package.json
  file. It's possible that the missing plugin is loaded by a preset
  you are using that forgot to add the plugin to its dependencies: you
  can workaround this problem by explicitly adding the missing package
  to your top-level package.json.
  `;
    throw error;
  }
  function tryRequireResolve(id, dirname) {
    try {
      if (dirname) {
        return {
          error: null,
          value: (((v, w) => (v = v.split("."), w = w.split("."), +v[0] > +w[0] || v[0] == w[0] && +v[1] >= +w[1]))(process.versions.node, "8.9") ? require.resolve : (r, {
            paths: [b]
          }, M = require("module")) => {
            let f = M._findPath(r, M._nodeModulePaths(b).concat(b));
            if (f) return f;
            f = new Error(`Cannot resolve module '${r}'`);
            f.code = "MODULE_NOT_FOUND";
            throw f;
          })(id, {
            paths: [dirname]
          })
        };
      } else {
        return {
          error: null,
          value: require.resolve(id)
        };
      }
    } catch (error) {
      return {
        error,
        value: null
      };
    }
  }
  function tryImportMetaResolve(id, options) {
    try {
      return {
        error: null,
        value: (0, _importMetaResolve.resolve)(id, options)
      };
    } catch (error) {
      return {
        error,
        value: null
      };
    }
  }
  function resolveStandardizedNameForRequire(type, name, dirname) {
    const it = resolveAlternativesHelper(type, name);
    let res = it.next();
    while (!res.done) {
      res = it.next(tryRequireResolve(res.value, dirname));
    }
    return res.value;
  }
  function resolveStandardizedNameForImport(type, name, dirname) {
    const parentUrl = (0, _url().pathToFileURL)(_path().join(dirname, "./babel-virtual-resolve-base.js")).href;
    const it = resolveAlternativesHelper(type, name);
    let res = it.next();
    while (!res.done) {
      res = it.next(tryImportMetaResolve(res.value, parentUrl));
    }
    return (0, _url().fileURLToPath)(res.value);
  }
  function resolveStandardizedName(type, name, dirname, resolveESM) {
    if (!_moduleTypes.supportsESM || !resolveESM) {
      return resolveStandardizedNameForRequire(type, name, dirname);
    }
    try {
      return resolveStandardizedNameForImport(type, name, dirname);
    } catch (e) {
      try {
        return resolveStandardizedNameForRequire(type, name, dirname);
      } catch (e2) {
        if (e.type === "MODULE_NOT_FOUND") throw e;
        if (e2.type === "MODULE_NOT_FOUND") throw e2;
        throw e;
      }
    }
  }
  {
    var LOADING_MODULES = new Set();
  }
  function* requireModule(type, name) {
    {
      if (!(yield* (0, _async.isAsync)()) && LOADING_MODULES.has(name)) {
        throw new Error(`Reentrant ${type} detected trying to load "${name}". This module is not ignored ` + "and is trying to load itself while compiling itself, leading to a dependency cycle. " + 'We recommend adding it to your "ignore" list in your babelrc, or to a .babelignore.');
      }
    }
    try {
      {
        LOADING_MODULES.add(name);
      }
      {
        return yield* (0, _moduleTypes.default)(name, `You appear to be using a native ECMAScript module ${type}, ` + "which is only supported when running Babel asynchronously.", true);
      }
    } catch (err) {
      err.message = `[BABEL]: ${err.message} (While processing: ${name})`;
      throw err;
    } finally {
      {
        LOADING_MODULES.delete(name);
      }
    }
  }
  0 && 0;
  
module.exports = plugins
module.exports = require("@babel/compat-data/plugins");
module.exports = pluginsFrom;
module.exports = require("./data/plugins.json");
'use strict';