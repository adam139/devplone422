.. contents::

Introduction
============

Talking about multi-language support in Plone is talk about
Products.LinguaPlone. It has been the defacto standard for managing translations
of Archetypes-based content types in Plone through the years. Somehow its
functionality never made its way into the Plone core and today is in legacy
status. Nowadays, Plone faces the rising of Dexterity content types and its
incoming adoption into the Plone core in the near future (4.3) and complete the
transition to Plone as default content types in Plone 5.

plone.app.multilingual was designed originally to provide Plone a whole
multilingual story. Using ZCA technologies, enables translations to Dexterity
and Archetypes content types as well managed via an unified UI.

This module provides the user interface for managing content translations. It's
the app package of the next generation Plone multilingual engine. It's designed
to work with Dexterity content types and the *old fashioned* Archetypes based
content types as well. It only works with Plone 4.1 and above due to the use of
UUIDs to reference the translations.

After more than 7 years, a GSOC, redesigns, reimplementations due to deprecated
libraries, two major Plone versions finally we are able to say that
plone.app.multilingual is finally here.

Components
==========

PAM is composed of four packages, two are mandatory:

    * plone.app.multilingual (UI)
    * plone.multilingual (core)

and two optionals (at least one should be installed):

    * plone.multilingualbehavior (enables Dexterity support via a behavior)
    * archetypes.multilingual (enables Archetypes support)

Usage
=====

To use this package with both Dexterity and Archetypes based content types you
should add the following two lines to your *eggs* buildout section::

    eggs =
        plone.app.multilingual
        plone.multilingualbehavior

If you need to use this package only with Archetypes based content types you
only need the following line::

    eggs =
        plone.app.multilingual


Setup
=====

After re-running your buildout and installing the newly available add-ons, you
should go to the *Languages* section of your site's control panel and select
at least two or more languages for your site. You will now be able to create
translations of Plone's default content types, or to link existing content as
translations.

Features
========

These are the most important features PAM provides.

Root Language folders
---------------------

After the setup, PAM will create root folders for each of your site's
languages and put translated content into the appropriate folders. A language
folder implements INavigationRoot, so from the user's point of view, each
language is "jailed" inside its correspondent language folder. There are
subscribers in place to capture user interaction with content and update the
language in contents accordingly, for example when user moves or copy content
between language folders.


Babel view
----------

An evolution of the LP *translate* view, unified for either Archetypes and
Dexterity content types. It features an already translated content viewer for
the current content being edited via an ajaxified dinamic selector that shows
them on the fly on user request.


Language independent fields
---------------------------

PAM has support for language independent fields, but with a twist respect the
LP implementation. As PAM does design does not give more relevance to one
translated object above the others siblings (has no canonical object), fields
marked as language independent get copied over all the members of the
translation group always. The PAM UI will warn you about this behavior by
reminding you that the values in the field on the other group participants
will be overwritten.


Translation locator policy
--------------------------

When translating content, this policy decides how it would be placed in the
site's structure. There are two policies in place:

    * LP way, the translation gets placed in the nearest translated folder in
      parent's hierarchy

    * Ask user where to place the translated element in the destination
      language root folder

Language selector policy
------------------------

While browsing the site, the language selector viewlet allows users to switch
site's content language and ease access between translations of the current
content. There are two policies in place in case the translation of a specific
language does not exist (yet):

    * LP way, the selector shows the nearest translated container.
    * Shows the user an informative view that shows the current available
      translations for the current content.


Neutral root folder support
---------------------------

The root language folders are used to place the tree of the correspondent
language content. However, there are some use cases we need content that does
not belongs to any language. For example, for assets or side resources like
images, videos and documents. There is need to maintain a language neutral
folder for place this kind of objects. After PAM setup, there is a special
folder called *Language shared*. All items placed in this folder will have
neutral as its default language and will be visible from the other root
language folders as they were placed there.


Translation map
---------------

In order to ease the translation tasks, we devised a tool that displays in a
useful way all the current translated objects and its current translation
information. The map also shows a list of missing translations in case you
want to build a *mirrored* (completely) translated site.


Google Translation Service integration
--------------------------------------

If you are subscriber of the Google Translation service (a paid service), you
can setup your API key on *Languages* site setup. Then, you will notice a new
icon in the babel view that takes the original field on the left side and
using Google Translations service, translates its contents and fill the right
side field.


LinguaPlone migration
---------------------

You can migrate your existing LP powered site to PAM using the *Migration* tab
in the *languages* control panel. This non-destructive procedure will copy the
translation information stored in content objects used by LP to the
translation storage structures used in PAM.


Backup
------

Sometimes, it can be handy to have at hand a procedure that dumps translation
information to an exportable format for later use. You can do so in the tab
*Backup* in *languages* control panel.

For information about making your Dexterity content type translatable, see the
plone.multilingualbehavior documentation.


Marking objects as translatables
================================

Archetypes
----------

By default, if PAM is installed, Archetypes-based content types are marked as
translatables


Dexterity
---------

Users should mark a dexterity content type as translatable by assigning a the
multilingual behavior to the definition of the content type either via file
system, supermodel or through the web.


Marking fields as language independant
======================================

Archetypes
----------

The language independent fields on Archetype-based content are marked the same
way as in LinguaPlone::

    atapi.StringField(
        'myField',
        widget=atapi.StringWidget(
        ....
        ),
        languageIndependent=True
    ),

.. note::

    If you want to completely remove LinguaPlone of your installation, you
    should make sure that your code are dependant in any way of LP.


Dexterity
---------

There are four ways of achieve it.

Grok directive
~~~~~~~~~~~~~~

In your content type class declaration::

    from plone.multilingualbehavior import directives
    directives.languageindependent('field')

Supermodel
~~~~~~~~~~

In your content type XML file declaration::

    <field name="myField" type="zope.schema.TextLine" lingua:independent="true">
        <description />
        <title>myField</title>
    </field>

Native
~~~~~~

In your code::

    from plone.multilingualbehavior.interfaces import ILanguageIndependentField
    alsoProvides(ISchema['myField'], ILanguageIndependentField)

Through the web
~~~~~~~~~~~~~~~

Via the content type definition in the *Dexterity Content Types* control panel.


Internal design of plone.multilingual
======================================

All the internal features are implemented on the package plone.multilingual.

The key points are:

    1. Each translation is a content object
    2. There is no canonical object
    3. The translation reference storage is external to the content
       object
    4. Adapt all the steps on translation
    5. Language get/set via an unified adapter
    6. Translatable marker interface(s)


There is no canonical content object
------------------------------------

Having a canonical object on the content space produces a dependency which is
not orthogonal with the normal behavior of Plone. Content objects should be
autonomous and you should be able to remove it. This is the reason because we
removed the canonical content object. There is a canonical object on the
translation infrastructure but is not on the content space.


Translation reference storage
-----------------------------

In order to maintain the relations between the different language objects we
designed a local utility that stores the relation tree on a BTree. The
relations with all the content are done using default Plone implementation of
UUIDs. We decided to push on that direction because:

    * UUID are the actual content object identifier
    * It's faster to access or modify one (or several) translation at once
      without waking objects
    * It's easier to work on all the translation (exports/imports)
    * It's easier to maintain the integrity of all the translations
    * It allows to access to the whole translation graph from one centralized
      point of view enabling other uses of this graph, for example, the
      translation map


Adapt all the steps on translation
----------------------------------

The different aspects involved on a translation are adapted, so it's possible
to create different policies for different types, sites, etc.

  * ITranslationFactory - General factory used to create a new content

    * ITranslationLocator - Where we are going to locate the new translated content

        Default : If the parent folder is translated create the content on the
        translated parent folder, otherwise create on the parent folder.

    * ITranslationCloner - Method to clone the original object to the new one

        Default : Nothing

    * ITranslationIdChooser - Which id is the translation

        Default : The original id + lang code-block

  * ILanguageIndependentFieldsManager - Manager for language independent fields

    Default: Nothing


Language get/set via an unified adapter
---------------------------------------

In order to access and modify the language of a content type regardless the
type (Archetypes/Dexterity) there is a interface/adapter::

    plone.multilingual.interfaces.ILanguage

You can use::

    from plone.multilingual.interfaces import ILanguage
    language = ILanguage(context).get_language()

or in case you want to set the language of a content::

    language = ILanguage(context).set_language('ca')


Translatable marker interface
-----------------------------

In order to know if a content can be translated there is a marker interface:

    plone.multilingual.interfaces.ITranslatable


License
=======

GNU General Public License, version 2


Roadmap
=======

This is the planned feature list for PAM:

1.0
---

    * Babel view
    * Root language folders
    * Translation locator policy
    * Language selector policy
    * Neutral root folder support
    * Translation map
    * Google Translation Service integration
    * LinguaPlone migration
    * Backup

2.0
---

    * XLIFF export/import
    * Iterate support: we know there are some needs about iterate integration
    * LinguaPlus/linguatools set of useful tools
    * Outdated translations alerts and translation workflows support

3.0
---

    * plone.app.toolbar/plone.app.cmsui support
    * Add support for Deco layouts and content types
    * Pluggable translation policies
    * Pluggable language policies negotiations
