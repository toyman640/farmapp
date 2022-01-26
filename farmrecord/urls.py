from django.urls import path
from farmrecord import views

app_name = 'farmrecord'

urlpatterns = [
    path('', views.index, name='index'),
    path('cow-claving/', views.cow_birth, name='cow_birth'),
    path('cow-culling', views.cow_cull, name='cow_cull'),
    path('cow-mortality', views.cow_motrep, name='cow_motrep'),
    path('cow-procurement', views.cow_proc, name='cow_proc'),
    path('cow-sales', views.cow_sales, name='cow_sales'),
    path('goat-birth', views.goat_birth, name='goat_birth'),
    path('goat-culling', views.goat_cull, name='goat_cull'),
    path('goat-mortality', views.goat_motrep, name='goat_motrep'),
    path('goat-procurement', views.goat_proc, name='goat_proc'),
    path('goat-sales', views.goat_sales, name='goat_sales'),
    path('pig-birth', views.pig_birth, name='pig_birth'),
    path('pig-culling', views.pig_cull, name='pig_cull'),
    path('pig-mortality', views.pig_motrep, name='pig_motrep'),
    path('pig-procurement', views.pig_proc, name='pig_proc'),
    path('pig-sales', views.pig_sales, name='pig_sales'),
    path('sheep-birth', views.sheep_birth, name='sheep_birth'),
    path('sheep-culling', views.sheep_cull, name='sheep_cull'),
    path('sheep-mortality', views.sheep_motrep, name='sheep_motrep'),
    path('sheep-procurement', views.sheep_proc, name='sheep_proc'),
    path('sheep-sales', views.sheep_sales, name='sheep_sales'),
    path('cow-motality-records', views.cow_motrec, name='cow_motrec'),
    path('cow-procurement-records', views.cow_procrec, name='cow_procrec'),
    path('cow-sale-records', views.cow_salerec, name='cow_salerec'),
    path('cow-cull-records', views.cow_cullrec, name='cow_cullrec'),
    path('goat-mortality-records', views.goat_motrec, name='goat_motrec'),
    path('goat-procurement-records', views.goat_procrec, name='goat_procrec'),
    path('goat-cull-records', views.goat_cullrec, name='goat_cullrec'),
    path('goat-sale-records', views.goat_salerec, name='goat_salerec'),
    path('sheep-mortality-records', views.sheep_motrec, name='sheep_motrec'),
    path('sheep-procurement-records', views.sheep_procrec, name='sheep_procrec'),
    path('sheep-cull-records', views.sheep_cullrec, name='sheep_cullrec'),
    path('sheep-sale-records', views.sheep_salerec, name='sheep_salerec'),
    path('pig-sale-records', views.pig_salerec, name='pig_salerec'),
    path('pig-mortality-records', views.pig_motrec, name='pig_motrec'),
    path('pig-procurement-records', views.pig_procrec, name='pig_procrec'),
    path('pig-cull-records', views.pig_cullrec, name='pig_cullrec'),
    path('cow-mortality-record-view/<int:abt_id>', views.cow_motrec_view, name='cow_motrec_view'),
    path('cow-culling-record-view/<int:abtc_id>', views.cow_cullrec_view, name='cow_cullrec_view'),
    path('cow-procurement-record-view/<int:abt_id>', views.cow_procrec_view, name='cow_procrec_view'),
    path('cow-sale-record-view/<int:abt_id>', views.cow_salerec_view, name='cow_salerec_view'),
    path('goat-mortality-record-view/<int:abt_id>', views.goat_motrec_view, name='goat_motrec_view'),
    path('goat-sale-record-view/<int:abt_id>', views.goat_salerec_view, name='goat_salerec_view'),
    path('goat-procurement-record-view/<int:abt_id>', views.goat_procrec_view, name='goat_procrec_view'),
    path('goat-cull-record-view/<int:abt_id>', views.goat_cullrec_view, name='goat_cullrec_view'),
    path('pig-cull-record-view/<int:abt_id>', views.pig_cullrec_view, name='pig_cullrec_view'),
    path('pig-mortality-record-view/<int:abt_id>', views.pig_motrec_view, name='pig_motrec_view'),
    path('pig-sale-record-view/<int:abt_id>', views.pig_salerec_view, name='pig_salerec_view'),
    path('pig-procurement-record-view/<int:abt_id>', views.pig_procrec_view, name='pig_procrec_view'),
    path('sheep-mortality-record-view/<int:abt_id>', views.sheep_motrec_view, name='sheep_motrec_view'),
    path('sheep-sale-record-view/<int:abt_id>', views.sheep_salerec_view, name='sheep_salerec_view'),
    path('sheep-cull-record-view/<int:abt_id>', views.sheep_cullrec_view, name='sheep_cullrec_view'),
    path('delete-post-cow/<int:listf_id>', views.delete_postc, name='delete_postc'),
    path('delete-post-goat/<int:listg_id>', views.delete_postg, name='delete_postg'),
    path('delete-post-sheep/<int:listf_id>', views.delete_posts, name='delete_posts'),
    path('delete-post-pig/<int:listf_id>', views.delete_postp, name='delete_postp'),
    path('delete-post-goat/<int:listcullg_id>', views.delete_postcullg, name='delete_postcullg'),
    path('delete-post-pig/<int:listcullp_id>', views.delete_postcullp, name='delete_postcullp'),
    path('delete-post-sheep/<int:listculls_id>', views.delete_postculls, name='delete_postculls'),
    path('delete-post-cow-culling/<int:listcullc_id>', views.delete_postcullc, name='delete_postcullc'),
    path('delete-post-sale-cow/<int:listsalec_id>', views.delete_postsalec, name='delete_postsalec'),
    path('delete-post-sale-goat/<int:listsaleg_id>', views.delete_postsaleg, name='delete_postsaleg'),
    path('delete-post-sale-pig/<int:listsalep_id>', views.delete_postsalep, name='delete_postsalep'),
    path('delete-post-sheep/<int:listsales_id>', views.delete_postsales, name='delete_postsales'),
    path('delete-post-proc-cow/<int:listprocc_id>', views.delete_postprocc, name='delete_postprocc'),
    path('delete-post-proc-goat/<int:listprocg_id>', views.delete_postprocg, name='delete_postprocg'),
    path('delete-post-proc-pig/<int:listprocp_id>', views.delete_postprocp, name='delete_postprocp'),
    path('delete-post-proc-sheep/<int:listprocs_id>', views.delete_postprocs, name='delete_postprocs'),
    path('edit-post-cow-mortality/<int:post_id>', views.edit_cowmot, name='edit_cowmot'),
    path('edit-post-goat-mortality/<int:post_id>', views.edit_goatmot, name='edit_goatmot'),
    path('edit-post-sheep-mortality/<int:post_id>', views.edit_sheepmot, name='edit_sheepmot'),
    path('edit-post-pig-mortality/<int:post_id>', views.edit_pigmot, name='edit_pigmot'),
    path('edit-post-cow-sale/<int:post_id>', views.edit_cowsale, name='edit_cowsale'),
    path('edit-post-goat-sale/<int:post_id>', views.edit_goatsale, name='edit_goatsale'),
    path('edit-post-pig-sale/<int:post_id>', views.edit_pigsale, name='edit_pigsale'),
    path('edit-post-sheep-sale/<int:post_id>', views.edit_sheepsale, name='edit_sheepsale'),
    path('edit-post-cow-proc/<int:post_id>', views.edit_cowproc, name='edit_cowproc'),
    path('edit-post-pig-proc/<int:post_id>', views.edit_pigproc, name='edit_pigproc'),
    path('edit-post-goat-proc/<int:post_id>', views.edit_goatproc, name='edit_goatproc'),
    path('edit-post-sheep-proc/<int:post_id>', views.edit_sheepproc, name='edit_sheepproc'),
    path('edit-post-cow-cull/<int:post_id>', views.edit_cowcull, name='edit_cowcull'),
    path('edit-post-pig-cull/<int:post_id>', views.edit_pigcull, name='edit_pigcull'),
    path('edit-post-goat-cull/<int:post_id>', views.edit_goatcull, name='edit_goatcull'),
    path('edit-post-sheep-cull/<int:post_id>', views.edit_sheepcull, name='edit_sheepcull'),
    path('cowmot-result/', views.cowmot_filter, name='cowmot_filter'),
    path('goatmot-result/', views.goatmot_filter, name='goatmot_filter'),
    path('pigmot-result/', views.pigmot_filter, name='pigmot_filter'),
    path('sheepmot-result/', views.sheepmot_filter, name='sheepmot_filter'),
    path('cowcull-result/', views.cowsale_filter, name='cowsale_filter'),
    path('pigcull-result/', views.pigsale_filter, name='pigsale_filter'),
    path('goatcull-result/', views.goatsale_filter, name='goatsale_filter'),
    path('sheepcull-result/', views.sheepsale_filter, name='sheepsale_filter'),
    path('cowcull-result/', views.cowcull_filter, name='cowcull_filter'),
    path('pigcull-result/', views.pigcull_filter, name='pigcull_filter'),
    path('sheepcull-result/', views.sheepcull_filter, name='sheepcull_filter'),
    path('goatcull-result/', views.goatcull_filter, name='goatcull_filter'),
    path('logout-view/', views.logout_view, name='logout_view'),
    path('cow-cencus/', views.cen_cow, name='cen_cow'),
    path('pig-census', views.cen_pig, name='cen_pig'),
    path('goat-cencus', views.cen_goat, name='cen_goat'),
    path('sheep-census', views.cen_sheep, name='cen_sheep'),
    path('cow-population-records', views.cencow_view, name='cencow_view'),
    path('goat-population-records', views.cengoat_view, name='cengoat_view'),
    path('pig-population-records', views.cenpig_view, name='cenpig_view'),
    path('sheep-population-records', views.censheep_view, name='censheep_view')
]

