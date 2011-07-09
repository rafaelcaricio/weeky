document.addEvent('domready', function() {

    var PlanningCell = new Class({
        initialize: function(element) {
            this.initElements(element);
            this.bindEvents();
        },

        initElements: function(element) {
            this.element = element;
            this.display = this.element.getElement(".planningCell_display");
            this.input = this.element.getElement("textarea");
        },

        bindEvents: function() {
            this.element.addEvents({
                mouseenter: this.mouseEnter.bind(this),
                mouseout: this.mouseOut.bind(this),
                click: this.fireInputFocus.bind(this),
                focus: this.fireInputFocus.bind(this)
            });

            this.input.addEvents({
                blur: this.toggleCell.bind(this)
            });
        },

        mouseEnter: function() {
            this.display.addClass("mouseover");
        },

        mouseOut: function() {
            this.display.removeClass("mouseover");
        },

        toggleCell: function() {
            this.display.toggleClass("hide");
            this.input.toggleClass("hide");
            this.display.set("html", this.input.get("value"));
        },
        
        fireInputFocus: function() {
            this.display.addClass("hide");
            this.input.removeClass("hide");
            this.input.focus();
        },

        getValue: function() {
            return this.input.get("value");
        }
    });

    $$('.planningCell_container').each(function(el) { 
        new PlanningCell(el);
    });
});
