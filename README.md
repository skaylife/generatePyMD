# Универсальный шаблон

## Структура папок и файлов

```
generateREADME/
    .gitignore
    main.py
    main.spec
    README.md
    requirements.txt
    .git/
        COMMIT_EDITMSG
        config
        description
        HEAD
        index
        hooks/
            applypatch-msg.sample
            commit-msg.sample
            fsmonitor-watchman.sample
            post-update.sample
            pre-applypatch.sample
            pre-commit.sample
            pre-merge-commit.sample
            pre-push.sample
            pre-rebase.sample
            pre-receive.sample
            prepare-commit-msg.sample
            push-to-checkout.sample
            update.sample
        info/
            exclude
        logs/
            HEAD
            refs/
                heads/
                    main
                remotes/
                    origin/
                        main
        objects/
            22/
                201f275fe22041773113c239a3d21787ae2157
            3c/
                c58fb7119e66e2d53105337e4aa9795eb67b74
            5e/
                0a05c5a5176c256d874423c50c3626d4e51772
            b8/
                4332eae6dc5216dbd4fc85a0a718cf9a9b6985
            e9/
                ab4a772ca4310521edf005fa778b56bdf308c1
            ef/
                a407c35ff028586b7ef5456c537971fefa5cea
            info/
            pack/
        refs/
            heads/
                main
            remotes/
                origin/
                    main
            tags/
    build/
        main/
            Analysis-00.toc
            base_library.zip
            EXE-00.toc
            main.pkg
            PKG-00.toc
            PYZ-00.pyz
            PYZ-00.toc
            warn-main.txt
            xref-main.html
            localpycs/
                pyimod01_archive.pyc
                pyimod02_importers.pyc
                pyimod03_ctypes.pyc
                pyimod04_pywin32.pyc
                struct.pyc
    dist/
        generatePyMD.exe
```

## Библиотеки

- altgraph==0.17.4
- CTkMessagebox==2.7
- customtkinter==5.2.2
- darkdetect==0.8.0
- packaging==24.1
- pefile==2023.2.7
- pillow==10.4.0
- pyinstaller==6.10.0
- pyinstaller-hooks-contrib==2024.8
- pywin32-ctypes==0.2.3
