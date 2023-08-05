import sys
from django.views.generic import ListView
from django.conf import settings
try:
    from django.apps import apps as models
except ImportError:
    from django.db import models
    
if not hasattr(models, 'get_model'):
    raise AttributeError('This version of Django does not have a method \
    "get_model" at the requested location')    


import base64

def encode_url(request):
    """This function is duplicated in *ImagePageContextMixin*, kept for
    backwards compatibility"""
    
    if sys.version_info[0] == 2:
        return base64.b64encode(request.META['PATH_INFO'])
    else:
        return base64.b64encode(bytes(request.META['PATH_INFO'], encoding='utf-8')).decode()

class ImagePageContextMixin(object):

    """Brings in context for lightbox."""

    def encode_url(self):
        if sys.version_info[0] == 2:
            return base64.b64encode(request.META['PATH_INFO'])
        else:
            return str(base64.b64encode(bytes(request.META['PATH_INFO'], encoding='utf-8')).decode())

    def get_context_data(self, *args, **kwargs):
        context = super(ImagePageContextMixin, self).get_context_data(*args, **kwargs)
        context['path'] = self.encode_url()
        return context

class ImagePageSettingsMixin(object):
    
    paginate_by = 1

    def image_clickable(self):
        return getattr(settings, 'LIGHTBOX_IMAGE_CLICKABLE', False)
        
    def get_styles(self):
        bgcolor = getattr(settings, 'LIGHTBOX_BG_COLOR', '#000')
        color = getattr(settings, 'LIGHTBOX_TXT_COLOR', '#fff')
        styles = {'bgcolor': bgcolor, 'color': color}
        return styles
    
    def get_factors(self):
        """
        Return multiplication factors for defining the relationship between 
        window height/width and the size of the image.
        """
        height_factor = getattr(settings, 'LIGHTBOX_VIEWABLE_HEIGHT_FACTOR', 0.85)
        width_factor = getattr(settings, 'LIGHTBOX_VIEWABLE_WIDTH_FACTOR', 0.85)
        
        height_ratio = getattr(settings, 'LIGHTBOX_IMAGE_WINDOW_HEIGHT_FACTOR', 0.71)
        width_ratio = getattr(settings, 'LIGHTBOX_IMAGE_WINDOW_WIDTH_FACTOR', 0.71)
        
        factors = {'view_height': height_factor,
                     'view_width': width_factor,
                     'height_ratio': height_ratio,
                     'width_ratio': width_ratio,
                     }
    
        return factors
    
    def get_lightbox_width_height(self):
        
        """
        Return dimensions for sorl thumbnail.
        """
        
        if self.request.is_mobile:
            lightbox_width = getattr(settings, 'LIGHTBOX_WIDTH_MOBILE', '800')
            lightbox_height = (int(lightbox_width) / 4) * 3 # aspect ratio 4 : 3 for ipad
        else:
            lightbox_width = getattr(settings, 'LIGHTBOX_WIDTH', '1600')
            lightbox_height = (int(lightbox_width) / 16) * 9 # aspect ration 16 : 9 for most others    
        return lightbox_width, 'x%d' % lightbox_height

class ImagePageMixin(object):
    """
    This is meant to be an alternative for a full screen lightbox.
    The browser should be doing the work (eg supporting mousewheel, touch events).
    
    The page should take:
    1) A url to return to when the user activates the close button
    2) A number of images in a series.
        
    """  
    def __init__(self):
        self.image_field_name = None
    
    def _get_related_of(self, model):
        """Get the most likely candidate field name from related model of the
        model arg, where ImageField has preference above FileField.
         
        @model parent model 
        """
        map_dict, map_list, relateds_list = {}, [], []
        
        # Get the field names and internal types of related model. The result
        # of this operation is a dict, where the *related_name* is the key
        # with the related models' fields and internal types as its value.
        # Example:
        # [{'images': [{'id': 'AutoField'},
        #    {'activiteit': 'ForeignKey'},
        #    {'bestand': 'FileField'},
        #    {'hoofdafbeelding': 'BooleanField'},
        #    {'onderschrift': 'CharField'},
        #    {'en_onderschrift': 'CharField'}]}]
        
        for key, val in model._meta.fields_map.items(): 
            map_dict[key]=[{f.name:f.get_internal_type()} \
                for f in val.related_model._meta.fields]
        
        # Refactor the python object to make it easier to handle.
        # Basically we are flattening the value of *map_dict_key* values, 
        # which is a list of dicts, into a straight dict, and appending the 
        # resultant object to *map_list*.
        # This is what the resultant object looks like:
        # [{'images': {'id': 'AutoField',
        #    'activiteit': 'ForeignKey',
        #    'bestand': 'FileField',
        #    'hoofdafbeelding': 'BooleanField',
        #    'onderschrift': 'CharField',
        #    'en_onderschrift': 'CharField'}}]
        
        for map_dict_key, map_dict_value in map_dict.items(): 
            map_list.append({ map_dict_key:dict((key, val) \
                for k in map_dict[map_dict_key] for key, val in k.items()) })
                
        # Go through the items in *map_list*, appending our objects of interest
        # to *relateds_list*.
        
        for item in map_list: 
            for map_dict_key, map_dict_value in item.items(): 
                for key, val in map_dict_value.items(): 
                    if val == 'ImageField': 
                        relateds_list.append ({ map_dict_key: key })
                    elif val == 'FileField': 
                        relateds_list.append ({ map_dict_key: key })
                    else:
                        pass
            if relateds_list:
                # return the first candidate. The result will be the first 
                # related_name with either an *ImageField* or a *FileField*
                # and will include the field name we are interested in.
                return relateds_list[0] 
            return None
        
    def get_queryset(self):
        
        # Get the model from the args, then also try to get the related model.
        model = models.get_model(self.kwargs['app'], self.kwargs['model'])
        print (model)
        pk = self.kwargs.get('pk', None)
        if not pk: # We are querying the main model
             qs = model.objects.filter(**filter_kwargs)
             return qs
        
        qs = model.objects.get(pk=self.kwargs['pk'])
        # take related_name from urls.py keyword arg, or if not given
        # do a lookup for the first related FileField or ImageField
        related_name = self.kwargs.get('related_name', None)
        
        if not related_name:
            related = self._get_related_of(model)
            related_name = list(related.keys())[0]
            self.image_field_name = list(related.values())[0]
        
        if not related_name:
            raise AttributeError('Current model does not have a related model')

        obj = getattr(qs, related_name) 
        return obj.all()
            
    def get_context_data(self, *args, **kwargs):
        context = super(ImagePageMixin, self).get_context_data(**kwargs)

        context['lightbox_width'] = self.get_lightbox_width_height()[0]
        context['lightbox_height'] = self.get_lightbox_width_height()[1]
        context['lightbox_image_clickable'] = self.image_clickable()
        context['factors'] = self.get_factors()
        context['styles'] = self.get_styles()
        
        context['app'] = self.kwargs['app']
        context['model'] = self.kwargs['model']
        context['pk'] = self.kwargs['pk']
        context['path'] = self.kwargs['path']
        context['image_field_name'] = self.image_field_name 
        
        if 'template' in self.kwargs.keys():
            self.template_name = self.kwargs['template']
        return context
    
    
    
class ImagePageView(ImagePageMixin, ImagePageSettingsMixin, ListView):
    template_name = 'lightbox/base.html'
