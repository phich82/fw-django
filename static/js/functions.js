var DATETIME_PICKER_CONFIG = {
    // format: 'DD/MM/YYYY HH:mm',
    format: 'DD/MM/YYYY',
    locale: 'en',
    icons: {
        time: 'glyphicon glyphicon-time',
        date: 'glyphicon glyphicon-calendar',
        up: 'glyphicon glyphicon-chevron-up',
        down: 'glyphicon glyphicon-chevron-down',
        previous: 'glyphicon glyphicon-chevron-left',
        next: 'glyphicon glyphicon-chevron-right',
        today: 'glyphicon glyphicon-screenshot',
        clear: 'glyphicon glyphicon-trash',
        close: 'glyphicon glyphicon-remove'
    },
    stepping: 0,
    showClear: true,
    showClose: true,
    timeZone: '',
    keepOpen: false,
    showTodayButton: true,
    toolbarPlacement: 'default', // default, top, bottom
};

function random(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function load(url, callback, identity) {
    if (typeof callback !== 'function') {
        identity = callback;
        callback = function(){};
    }
    var processResponse = function(response, status, xhr, container) {
        if (status == 'error') {
            return callback(false, xhr.status + ' ' + xhr.statusText);
        }
        return callback(true, response, container);
    };
    if ($(identity).length > 0) {
        return $(identity).load(url, function(response, status, xhr) {
            processResponse(response, status, xhr, $(identity).get(0));
        });
    }
    var container = createElement('div', {[identity.charAt(0) == '#' ? 'id' : 'className']: identity});
    return $(container).load(url, function(response, status, xhr) {
        processResponse(response, status, xhr, container);
    });
}

function createElement(name, options) {
    let container = document.createElement(name || 'div');
    // Add attributes to element
    if (options && typeof options === 'object') {
        Object.keys(options).forEach(function(key) {
            container[key] = options[key];
        });
    }
    document.body.appendChild(container);
    return container;
}

/****************** MODALS ******************/
function showModal(title, content, options, onclose, onsave) {
    let identity = '#modal-' + (new Date().getTime()) + '.' + random(10, 1000);
    let _options = {
        save_btn: false,
        close_btn: true,
        save_text: 'Save',
        close_text: 'Close',
    };

    /**
     * showModal(title, content, function onclose(hide){})
     */
    if (typeof options === 'function') {
        onclose = options
        onsave = null
    }
    /**
     * showModal(title, content, { save_btn: true }, function onclose(hide){}, function onsave(hide) {})
     */
    else if (typeof options === 'object') {
        _options = Object.assign(_options, options);
        /**
         * showModal(title, content, { save_btn: true }, function onsave(hide){})
         */
        if (_options.save_btn && typeof onsave !== 'function' && typeof onclose === 'function') {
            onsave = onclose;
            onclose = null;
        }
    }

    load('/static/html/popup.html', function(success, response, container) {
        if (!success) {
            alert('Could not load the popup template (templates/popup.html): ' + response);
            console.log('Could not load the popup template (popup.html): ' + response);
            return;
        }
        function _alignCenterPopup() {
            var winH = $(window).height();
            var winW = $(window).width();
            var popupShadow = $(container).find('.popup-shadow');
            // Set the popup window to center
            popupShadow.css('top',  winH/2-popupShadow.height()/2);
            popupShadow.css('left', winW/2-popupShadow.width()/2);
        }
        function _showPopup() {
            // Change popup title, content
            $(container).find('.popup-title').html(title || 'Title');
            $(container).find('.popup-message').html(content || '');

            if (!_options.save_btn) {
                $(container).find('.popup-save-btn').remove();
            } else {
                $(container).find('.popup-save-btn').html(_options.save_text || 'Save');
            }
            if (!_options.close_btn) {
                $(container).find('.popup-close-btn').remove();
            } else {
                $(container).find('.popup-close-btn').html(_options.close_text || 'Close');
            }

            // Display popup
            $(container).find('.popup').show();
            $(container).find('.popup-shadow').show();
            // Enable draggable
            $(container).find('.popup-shadow').draggable({cursor: 'move', containment: 'window'});
            // Align popup to center
            _alignCenterPopup();
        }
        $(window).resize(function() {
            _alignCenterPopup();
        });

        function _closePopup() {
            $(container).find('.popup').hide();
            $(container).find('.popup-shadow').hide();
            document.body.removeChild(container);
        }
        // Save button
        $(container).find('.popup-save').on('click', function() {
            (typeof onsave === 'function')
                ? onsave(_closePopup)
                : _closePopup();
        });
        // Close popup & remove the popup from DOM
        $(container).find('.popup-close').on('click', function() {
            (typeof callback === 'function')
                ? callback(_closePopup)
                : _closePopup();
        });
        _showPopup();
    }, identity);
}
/****************** END - MODALS ******************/

function isHexColor(color, both) {
    both = typeof both === 'boolean' ? both : false;
    pattern = both ? /^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})/gi : /^#[a-fA-F0-9]{6}/gi
    return pattern.test(color);
}

function customSelect(classSelect) {
    classSelect = classSelect || 'custom-select'
    var totalOption, elementSelect, div1, div2, div3;

    /* Look for any elements with the class "custom-select" */
    var containers = document.getElementsByClassName(classSelect);
    var totalSelect = containers.length;

    for (var i = 0; i < totalSelect; i++) {
        elementSelect = containers[i].getElementsByTagName("select")[0];
        totalOption = elementSelect.length;

        /* For each element, create a new DIV that will act as the selected item */
        div1 = document.createElement("DIV");
        div1.setAttribute("class", "select-selected");
        div1.innerHTML = elementSelect.options[elementSelect.selectedIndex].innerHTML;
        containers[i].appendChild(div1);

        /* For each element, create a new DIV that will contain the option list */
        div2 = document.createElement("DIV");
        div2.setAttribute("class", "select-items select-hide");

        for (var j = 1; j < totalOption; j++) {
            /* For each option in the original select element, create a new DIV that will act as an option item */
            div3 = document.createElement("DIV");
            div3.innerHTML = elementSelect.options[j].innerHTML;
            div3.addEventListener("click", function(e) {
                /* When an item is clicked, update the original select box, and the selected item */
                var select = this.parentNode.parentNode.getElementsByTagName("select")[0];
                var totalOption = select.length;
                var div1 = this.parentNode.previousSibling;

                for (var i = 0; i < totalOption; i++) {
                    // Update the selected option of select tag that its value equals to the selected item
                    if (select.options[i].innerHTML == this.innerHTML) {
                        // Update option selected
                        select.selectedIndex = i;
                        // Show value of selected option in DIV1
                        div1.innerHTML = this.innerHTML;
                        // Remove div3 that it has 'class' attribute as 'same-as-selected'
                        var div3 = this.parentNode.getElementsByClassName("same-as-selected");
                        var totalDIV3 = div3.length;
                        for (var k = 0; k < totalDIV3; k++) {
                            div3[k].removeAttribute("class");
                        }
                        // Add class="same-as-selected" to the selected current item
                        this.setAttribute("class", "same-as-selected");
                        break;
                    }
                }
                div1.click();
            });
            // Add all values of options of select (DIV3) tag to DIV2
            div2.appendChild(div3);
        }

        containers[i].appendChild(div2);

        div1.addEventListener("click", function(e) {
            /* When the select box is clicked, close any other select boxes, and open/close the current select box */
            e.stopPropagation();
            closeAllSelect(this);
            this.nextSibling.classList.toggle("select-hide");
            this.classList.toggle("select-arrow-active");
        });
    }

    function closeAllSelect(element) {
        /* Function that will close all select boxes in the document, except the current select box */
        var x, y, i, xl, yl, arrNo = [];
        x = document.getElementsByClassName("select-items");
        y = document.getElementsByClassName("select-selected");
        xl = x.length;
        yl = y.length;
        for (i = 0; i < yl; i++) {
            if (element == y[i]) {
                arrNo.push(i)
            } else {
                y[i].classList.remove("select-arrow-active");
            }
        }
        for (i = 0; i < xl; i++) {
            if (arrNo.indexOf(i)) {
                x[i].classList.add("select-hide");
            }
        }
    }
    /* If the user clicks anywhere outside the select box, then close all select boxes */
    document.addEventListener("click", closeAllSelect);
}

function customSelectJQuery(classSelect) {
    // Iterate over each select element
    $(classSelect || 'select').each(function() {

        // Cache the number of options
        var $this = $(this),
            totalOption = $(this).children('option').length;

        // Hide the select element
        $this.addClass('s-hidden');

        // Wrap the select element in a div
        $this.wrap('<div class="select"></div>');

        // Insert a styled div to sit over the top of the hidden select element
        $this.after('<div class="styledSelect"></div>');

        // Cache the styled div
        var $styledSelect = $this.next('div.styledSelect');

        // Show the first select option in the styled div
        $styledSelect.text($this.children('option').eq(0).text());

        // Insert an unordered list after the styled div and also cache the list
        var $list = $('<ul />', { 'class': 'options' }).insertAfter($styledSelect);

        // Insert a list item into the unordered list for each select option
        for (var i = 0; i < totalOption; i++) {
            $('<li />', {
                text: $this.children('option').eq(i).text(),
                rel: $this.children('option').eq(i).val()
            }).appendTo($list);
        }

        // Cache the list items
        var $listItems = $list.children('li');

        // Show the unordered list when the styled div is clicked (also hides it if the div is clicked again)
        $styledSelect.click(function (e) {
            e.stopPropagation();
            $('div.styledSelect.active').each(function () {
                $(this).removeClass('active').next('ul.options').hide();
            });
            $(this).toggleClass('active').next('ul.options').toggle();
        });

        // Hides the unordered list when a list item is clicked and updates the styled div to show the selected list item
        // Updates the select element to have the value of the equivalent option
        $listItems.click(function (e) {
            e.stopPropagation();
            $styledSelect.text($(this).text()).removeClass('active');
            $this.val($(this).attr('rel'));
            $list.hide();
        });

        // Hides the unordered list when clicking outside of it
        $(document).click(function () {
            $styledSelect.removeClass('active');
            $list.hide();
        });

    });
}
