App.Band = DS.Model.extend({
	name: DS.attr('string')
});

App.Band.FIXTURES = [
    {
        id: 1,
        name: 'The Front Bottoms'
    }
];