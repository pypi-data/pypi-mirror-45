/* The following line defines global variables defined elsewhere. */
/*globals require*/


if(require === undefined){
  require = function(reqs, torun){
    'use strict';
    return torun(window.jQuery);
  };
}

require([
  'jquery',
], function($) {
  'use strict';

    $.fn.toggleAttr = function(attr, attr1, attr2) {
        return this.each(function() {
            var self = $(this);
            if (self.attr(attr) == attr1)
                self.attr(attr, attr2);
            else
                self.attr(attr, attr1);
        });
    };

    $(document).click(function(event) {
        var nav = $('nav.action');
        if(!$(event.target).closest(nav).length) {
            jQuery(nav).children('ul.actionMenu').removeClass('activated').addClass('deactivated');
            jQuery(nav).children('ul.actionMenu').find('.actionMenuHeader').attr('aria-expanded', 'false');
            jQuery(nav).children('ul.actionMenu').find('.actionMenuContent').attr('aria-hidden', 'true');
        }
    });

    function toggleMenuHandler(event) {
        // swap between activated and deactivated
        jQuery(this).siblings().removeClass('activated').addClass('deactivated');
        jQuery(this).siblings().find('.actionMenuHeader').attr('aria-expanded', 'false');
        jQuery(this).siblings().find('.actionMenuContent').attr('aria-hidden', 'true');
        jQuery(this).toggleClass('deactivated activated');
        jQuery(this).find('.actionMenuHeader').toggleAttr('aria-expanded', 'true', 'false');
        jQuery(this).find('.actionMenuContent').toggleAttr('aria-hidden', 'true', 'false');
    }

    function initializeMenus() {
        // add toggle function to header links
        jQuery('ul.actionMenu')
            .click(toggleMenuHandler);
    }

    jQuery(initializeMenus);

});
