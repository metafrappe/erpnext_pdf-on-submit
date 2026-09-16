"""Focused regressions for the v16 ports. External AI/AWS calls are simulated."""
import importlib
import io
import queue
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import frappe
from frappe.model.base_document import get_controller


def run(app):
    assert app in frappe.get_installed_apps()
    modules = frappe.get_all('Module Def', filters={'app_name': app}, pluck='name')
    doctypes = frappe.get_all('DocType', filters={'module': ['in', modules]}, pluck='name')
    for doctype in doctypes:
        frappe.get_meta(doctype)
        get_controller(doctype)
    globals()['check_' + app]()
    print({'app': app, 'controllers': len(doctypes), 'regressions': 'passed'})


def run_unittests(module):
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(importlib.import_module(module)))
    assert result.testsRun > 0 and result.wasSuccessful(), module


def check_pdf_on_submit():
    run_unittests('pdf_on_submit.tests.test_quill')
