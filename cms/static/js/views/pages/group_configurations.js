define([
    'jquery', 'underscore', 'gettext', 'js/views/baseview',
    'js/views/group_configurations_list'
],
function ($, _, gettext, BaseView, GroupConfigurationsList) {
    'use strict';
    var GroupConfigurationsPage = BaseView.extend({
        initialize: function() {
            BaseView.prototype.initialize.call(this);
            this.listView = new GroupConfigurationsList({
                collection: this.collection
            });
        },

        render: function() {
            this.hideLoadingIndicator();
            this.$('.content-primary').append(this.listView.render().el);
            this.addButtonActions();
            this.addWindowActions();
            this.focusOnElement();
        },

        addButtonActions: function () {
            this.$('.nav-actions .new-button').click(function (event) {
                this.listView.addOne(event);
            }.bind(this));
        },

        addWindowActions: function () {
            $(window).on('beforeunload', this.onBeforeUnload.bind(this));
        },

        onBeforeUnload: function () {
            var dirty = this.collection.find(function(configuration) {
                return configuration.isDirty();
            });

            if(dirty) {
                return gettext(
                    'You have unsaved changes. Do you really want to leave this page?'
                );
            }
        },

        getLocationHash: function() {
            return window.location.hash;
        },

        focusOnElement: function () {
            var hash = this.getLocationHash(), focusedModel;

            if (hash) {
                focusedModel = this.collection.findWhere(
                    {id: parseInt(hash.replace('#', ''))}
                );
                focusedModel.set('showGroups', true);
                this.$(hash).focus();
            }
        }
    });

    return GroupConfigurationsPage;
}); // end define();
