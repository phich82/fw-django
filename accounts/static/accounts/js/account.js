$(function() {
    $('#start_date').datetimepicker(Object.assign(DATETIME_PICKER_CONFIG, {

    })).on('dp.change', function(e) {
        console.log('e => ', e)
    });

    $('#end_date').datetimepicker(Object.assign(DATETIME_PICKER_CONFIG, {

    })).on('dp.change', function(e) {
        console.log('e => ', e)
    });

    var id = 1;
    showModal('Confirmation', 'Are you sure to want delete this record?', { save_btn: true },
        function onsave(hide) {
            $.ajax({
                url: window.location.href,
                type: 'DELETE',
                contentType: 'json',
                // NOTES: MUST BE A JSON STRING
                data: JSON.stringify({
                    "id": id,
                }),
                success: function(result) {
                    console.log('result => ', result)
                    let message = 'The csv file has been successfully deleted.'
                    if (!result.success) {
                        message = result.error
                    } else {
                        // $('.csv-'+id).remove()
                        $('.csv-list').html(result.csv_table_html)
                        $('.pagination-links').html(result.pagination_links)
                    }
                    showModal('Upload Csv', message);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    showModal('Upload Csv', 'Could not delete the csv file. Error: ' + errorThrown);
                }
            });
            hide();
        }
    );
})
