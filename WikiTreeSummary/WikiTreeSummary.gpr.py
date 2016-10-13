register(QUICKREPORT,
         id    = 'WikiTreeSummary',
         name  = _("WikiTree Summary of a Person"),
         description= _("Display a summary of a person suitable for pasting into the Biography on WikiTree."),
         version = '0.1.0',
         gramps_target_version = "4.2",
         status = STABLE,
         fname = 'WikiTreeSummary.py',
         authors = ["John Ralls"],
         authors_email = ["jralls@ceridwen.us"],
         category = CATEGORY_QR_PERSON,
         runfunc = 'run'
  )
