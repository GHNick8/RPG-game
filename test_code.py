'''
SETUP LOGIC main.py

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Toggle save menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            save_menu.toggle()

        # Pass event to save menu if it's open
        if save_menu.active:
            result = save_menu.handle_event(event)
            if result == "saved":
                print("Game saved!")
            elif result == "loaded":
                print("Game loaded!")
            continue 

        # Shop input 
        if shop_menu.is_active():
            shop_menu.handle_event(event)

        # Interact with shopkeeper
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if player.rect.colliderect(shopkeeper.rect):
                shop_menu.open()

        # Inventory test keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print(inventory.use_item("Potion", player))
            elif event.key == pygame.K_o:
                print(inventory.buy_item("Potion"))
            elif event.key == pygame.K_g:
                inventory.gold += 50
                print("Added 50 gold!")

        # Battle input
        if in_battle and battle:
            battle.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_b and not in_battle:
            in_battle = True
            battle = BattleScene(player)

        # Player menu 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player_menu.active = not player_menu.active
            elif player_menu.active and event.key in (pygame.K_z, pygame.K_RETURN):
                player_menu.active = False

    # Update + Draw
    screen.fill(BG_COLOR)

    if in_battle and battle:
        battle.update()
        battle.draw(screen)

        if battle.ready_to_exit:
            in_battle = False
            battle = None

    else:
        if not shop_menu.is_active() and not save_menu.active and not player_menu.active:
            encounter = player.handle_input(game_map)
            if encounter == "encounter":
                in_battle = True
                battle = BattleScene(player)

        # Draw world
        game_map.draw(screen)
        player.draw(screen)
        shopkeeper.draw(screen)

        # Player menu
        player_menu.draw(screen)

        # Shop menu
        if shop_menu.is_active():
            shop_menu.draw(screen)

        # Shop dialog box
        if shop_menu.is_active():
            shop_menu.draw(screen)

        # Save menu
        if save_menu.active:
            save_menu.draw(screen)

    pygame.display.update()
    clock.tick(FPS) '''