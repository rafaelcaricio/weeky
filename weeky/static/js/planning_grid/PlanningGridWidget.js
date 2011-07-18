document.addEvent('domready', function() {

    var PlanningCell = new Class({
        initialize: function(element) {
            this.initElements(element);
            this.bindEvents();
            this.element.store("self", this);
        },

        initElements: function(element) {
            this.blocked = false;
            this.element = element;
            this.tabHandler = this.element.getElement(".tabHandler");
            this.display = this.element.getElement(".planningCell_display");
            this.input = this.element.getElement("textarea");
        },

        bindEvents: function() {
            this.element.addEvents({
                mouseenter: this.mouseEnter.bind(this),
                mouseout: this.mouseOut.bind(this),
                click: this.fireInputFocus.bind(this),
            });

            this.tabHandler.addEvents({
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
            if (!this.blocked) {
                this.display.addClass("hide");
                this.input.removeClass("hide");
                this.input.focus();
            }
            this.blocked = false;
        },

        blockFocus: function() {
            this.display.removeClass("mouseover");
            this.blocked = true;
        },

        getValue: function() {
            return this.input.get("value").trim();
        },

        setValue: function(value) {
            this.input.set("value", value);
            this.display.set("html", this.input.get("value"));
        }
    });

    var PlanningGrid = new Class({
        initialize: function() {
            $$('.planningCell_container').each(function(el) {
                new PlanningCell(el);
            });

            $$(".planningCell_display").makeDraggable({
                droppables: $$(".planningCell_container"),

                onStart: function(draggable, droppable) {
                    draggable.addClass('planningGrid_drag');
                },

                onEnter: function(draggable, droppable) {
                    droppable.retrieve("self").display.addClass('planningGrid_dragto');
                },

                onLeave: function(draggable, droppable) {
                    droppable.retrieve("self").display.removeClass('planningGrid_dragto');
                },

                onDrop: function(draggable, droppable) {
                    if (droppable) {
                        var dropl = droppable.retrieve("self");
                        var dragl = draggable.getParent().retrieve("self");
                        var response = true;
                        if (dropl.getValue() != "") {
                            response = confirm("You really want to override this value?");
                        }
                        if (response) {
                            dropl.setValue(dragl.getValue().trim());
                            dragl.setValue("");
                            dragl.blockFocus();
                        }
                        dropl.display.removeClass('planningGrid_dragto');
                    }
                },

                onComplete: function(draggable, droppable) {
                    draggable.removeClass("planningGrid_drag");
                    draggable.setStyle("top", 0);
                    draggable.setStyle("left", 0);
                }
            });
        }
    });

    new PlanningGrid();
});
