import prep_func
import my_tokens as mt

photo_count = prep_func.get_photo_count()
photo_owner = prep_func.get_photo_owner()
photo_info = prep_func.get_photo_info(photo_owner, photo_count, mt.vk_access_token)
prep_func.write_json(photo_info)
prep_func.yd_disk_folder_create(mt.yd_access_token)
prep_func.yd_disk_upload_photo(mt.yd_access_token, photo_info)
