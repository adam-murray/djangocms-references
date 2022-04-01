

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from cms.api import add_plugin, create_page, create_title
from cms.test_utils.testcases import CMSTestCase

from djangocms_alias.models import Alias as AliasModel, AliasContent, Category
from djangocms_alias.utils import is_versioning_enabled


class AliasReferencesIntegrationTestCase(CMSTestCase):
    def test_menucontent_references_integration(self):
        """
        When opening the references for a given alias, the objects which reference it should be listed
        """
        user = self.get_superuser()
        category = Category.objects.create(name="References Integration Alias Category")
        alias = AliasModel.objects.create(
            category=category,
            position=0,
        )
        AliasContent.objects.create(
            alias=alias,
            name="Alias Content",
            language="en",
        )
        kwargs = {}
        if is_versioning_enabled():
            kwargs = {"created_by": user}
        page = create_page(
            title="References Integration Page",
            template="page.html",
            language="en",
            menu_title="",
            in_navigation=True,
            **kwargs
        )
        if is_versioning_enabled():
            page_content = create_title("en", "Draft Page", page, created_by=user)
        else:
            page_content = page.pagecontent_set.last()
        placeholder = page_content.get_placeholders().get(
            slot="content"
        )
        alias_plugin = add_plugin(
            placeholder,
            "Alias",
            language="en",
            template="default",
            alias=alias,
        )

        alias_content_type = ContentType.objects.get(app_label="djangocms_alias", model="alias")
        references_endpoint = reverse(
            "djangocms_references:references-index",
            kwargs={"content_type_id": alias_content_type.id, "object_id": alias.id}
        )
        with self.login_user_context(user):
            response = self.client.get(references_endpoint)

        self.assertContains(response, alias.name)
        self.assertContains(response, alias_plugin.plugin_type.lower())