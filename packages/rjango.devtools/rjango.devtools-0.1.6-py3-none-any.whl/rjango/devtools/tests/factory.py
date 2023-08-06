from django.test import TestCase


class FactoryModelBaseTest(TestCase):
    def setUp(self, **kwargs):
        self.factory = kwargs['factory']
        self.model = self.factory._meta.model
        self.db_obj = self.factory()

    def test_model_exists(self):
        obj = self.db_obj
        status = self.model.STATUS.UNVERIFIED.value

        ###
        # Test against the object in the database not whats in memory.
        db_obj = self.model.objects.filter(uuid=obj.uuid)
        self.assertTrue(db_obj.exists())
        ###

        db_obj = db_obj.first()

        ##
        # Confirm fresh customer model is what we expect.
        self.assertEqual(obj.uuid, db_obj.uuid)
        self.assertEqual(obj.verified_email, False)
        ##

        self.assertEqual(obj.status, status)

    def test_model_create_batch(self):
        self.factory.create_batch(3)
