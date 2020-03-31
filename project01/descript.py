from underthesea import sent_tokenize

category = ['thoi_su', 'goc_nhin', 'the_gioi', 'kinh_doanh', 'giai_tri', 'the_thao', 'phap_luat', 'giao_duc', 'suc_khoe', 'doi_song',
            'du_lich', 'khoa_hoc', 'so_hoa', 'xe', 'y_kien', 'tam_su']

for cat in category:
    with open('article/'+cat+'.txt', 'r', encoding='utf-8') as article:
        with open('data/'+cat+ '/' + cat + '_description.txt', 'w', encoding='utf-8') as desFile:
            desFile.write(article.readline())
            fullText = article.read()
            fullText = sent_tokenize(fullText)
            for i in range(len(fullText)):
                desFile.write(cat + '_' + str(i) + '.wav\n')
                desFile.write(fullText[i]+'\n')