const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

function control(value = '') {
  return {
    value,
    listeners: {},
    addEventListener(name, callback) { this.listeners[name] = callback; },
    emit(name) { this.listeners[name](); },
  };
}

const search = control();
const type = control();
const island = control();
const count = { textContent: '' };
const items = [
  { textContent: 'Bluefin tuna', dataset: { type: 'fish', island: 'north' }, hidden: false },
  { textContent: 'Blue crab', dataset: { type: 'crab', island: 'south' }, hidden: false },
  { textContent: 'Golden tuna', dataset: { type: 'fish', island: 'south' }, hidden: false },
];
const byId = {
  'catalog-search': search,
  'catalog-type': type,
  'catalog-island': island,
  'catalog-count': count,
};

vm.runInNewContext(fs.readFileSync('assets/catalog.js', 'utf8'), {
  document: {
    getElementById(id) { return byId[id]; },
    querySelectorAll() { return items; },
  },
});

const visible = () => items.filter((item) => !item.hidden).map((item) => item.textContent);
assert.deepEqual(visible(), ['Bluefin tuna', 'Blue crab', 'Golden tuna']);

search.value = 'BLUE tuna';
search.emit('input');
assert.deepEqual(visible(), ['Bluefin tuna']);

type.value = 'fish';
island.value = 'south';
type.emit('change');
island.emit('change');
assert.deepEqual(visible(), []);
assert.match(count.textContent, /^No items match\./);

search.value = '';
type.value = '';
island.value = '';
search.emit('input');
type.emit('change');
island.emit('change');
assert.deepEqual(visible(), ['Bluefin tuna', 'Blue crab', 'Golden tuna']);
console.log('catalog filtering assertions passed');
