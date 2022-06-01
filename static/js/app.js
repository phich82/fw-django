$.ajaxSetup({
    headers: {
        // "X-Requested-With": "XMLHttpRequest",
        'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
    }
});

/***************** FOR TEST I18N (FRONTEND) ****************/
console.log('gettext => ', gettext('this is to be translated'))
// interpolate
const data = {
    count: 10,
    total: 50
};
const formats = ngettext(
    'Total: %(total)s, there is %(count)s object',
    'there are %(count)s of a total of %(total)s objects',
    data.count
);
const string = interpolate(formats, data, true);
console.log('string => ', string)
/***************** END - FOR TEST I18N (FRONTEND) ****************/
