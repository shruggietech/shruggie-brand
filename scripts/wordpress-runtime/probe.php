<?php
/** WordPress-side integration assertions for a generated BrandBuilder theme. */

$phase = isset( $args[0] ) ? $args[0] : 'baseline';
$slug = 'stbb-go-schedule';
$theme = wp_get_theme();
if ( $theme->get_stylesheet() !== $slug || ! wp_is_block_theme() ) {
	throw new RuntimeException( 'Generated block theme is not active.' );
}
$settings = wp_get_global_settings();
$palette = $settings['color']['palette']['theme'] ?? array();
$palette_slugs = array_column( $palette, 'slug' );
foreach ( array( 'stbb-go-schedule-identity-primary', 'stbb-go-schedule-cue-action', 'stbb-go-schedule-text-primary' ) as $required ) {
	if ( ! in_array( $required, $palette_slugs, true ) ) {
		throw new RuntimeException( 'Missing resolved palette entry: ' . $required );
	}
}
$patterns = WP_Block_Patterns_Registry::get_instance()->get_all_registered();
$matched = array_values( array_filter( $patterns, static function ( $pattern ) {
	return str_starts_with( $pattern['name'], 'stbb-go-schedule/' );
} ) );
if ( count( $matched ) !== 4 ) {
	throw new RuntimeException( 'Expected four registered starter patterns.' );
}
$pattern_order = array( 'hero', 'text-media', 'features', 'contact' );
usort( $matched, static function ( $left, $right ) use ( $pattern_order ) {
	return array_search( basename( $left['name'] ), $pattern_order, true ) <=> array_search( basename( $right['name'] ), $pattern_order, true );
} );
if ( ! WP_Block_Styles_Registry::get_instance()->is_registered( 'core/group', 'stbb-go-schedule-card' ) ) {
	throw new RuntimeException( 'Brand card block style was not registered.' );
}
$variations = WP_Theme_JSON_Resolver::get_style_variations();
if ( ! array_filter( $variations, static function ( $variation ) {
	return ( $variation['title'] ?? null ) === 'Dark interface';
} ) ) {
	throw new RuntimeException( 'Approved dark Site Editor variation was not registered.' );
}
foreach ( $matched as $pattern ) {
	$blocks = parse_blocks( $pattern['content'] );
	if ( ! $blocks || parse_blocks( serialize_blocks( $blocks ) ) !== $blocks ) {
		throw new RuntimeException( 'Pattern block serialization failed: ' . $pattern['name'] );
	}
}
$page = get_page_by_path( 'stbb-fixture-page' );
if ( $phase === 'baseline' ) {
	$content = implode( "\n", array_column( $matched, 'content' ) );
	$id = wp_insert_post( array( 'ID' => $page ? $page->ID : 0, 'post_type' => 'page', 'post_status' => 'publish', 'post_title' => 'Fixture page', 'post_name' => 'stbb-fixture-page', 'post_content' => $content ), true );
	if ( is_wp_error( $id ) ) {
		throw new RuntimeException( $id->get_error_message() );
	}
	$existing_styles = get_page_by_path( 'wp-global-styles-' . $slug, OBJECT, 'wp_global_styles' );
	$styles = wp_insert_post( array( 'ID' => $existing_styles ? $existing_styles->ID : 0, 'post_type' => 'wp_global_styles', 'post_status' => 'publish', 'post_title' => 'Client override', 'post_name' => 'wp-global-styles-' . $slug, 'post_content' => wp_json_encode( array( 'version' => 3, 'isGlobalStylesUserThemeJSON' => true, 'styles' => array( 'color' => array( 'background' => '#101820', 'text' => '#ffffff' ) ) ) ) ), true );
	if ( is_wp_error( $styles ) ) {
		throw new RuntimeException( $styles->get_error_message() );
	}
	$assigned = wp_set_object_terms( $styles, $slug, 'wp_theme' );
	if ( is_wp_error( $assigned ) ) {
		throw new RuntimeException( $assigned->get_error_message() );
	}
	wp_clean_theme_json_cache();
	$footer = get_page_by_path( 'footer', OBJECT, 'wp_template_part' );
	$footer_id = wp_insert_post( array( 'ID' => $footer ? $footer->ID : 0, 'post_type' => 'wp_template_part', 'post_status' => 'publish', 'post_title' => 'Client footer', 'post_name' => 'footer', 'post_content' => '<!-- wp:paragraph --><p>Client footer preserved</p><!-- /wp:paragraph -->' ), true );
	if ( is_wp_error( $footer_id ) ) {
		throw new RuntimeException( $footer_id->get_error_message() );
	}
	$footer_terms = wp_set_object_terms( $footer_id, $slug, 'wp_theme' );
	if ( is_wp_error( $footer_terms ) ) {
		throw new RuntimeException( $footer_terms->get_error_message() );
	}
	$page = get_post( $id );
} elseif ( ! $page || ! str_contains( $page->post_content, 'Tell your story' ) ) {
	throw new RuntimeException( 'Client page did not survive theme replacement.' );
}
$override = get_page_by_path( 'wp-global-styles-' . $slug, OBJECT, 'wp_global_styles' );
if ( ! $override || ! str_contains( $override->post_content, '#101820' ) ) {
	throw new RuntimeException( 'Saved Global Styles override did not survive.' );
}
$effective_styles = wp_get_global_styles();
if ( ( $effective_styles['color']['background'] ?? null ) !== '#101820' || ( $effective_styles['color']['text'] ?? null ) !== '#ffffff' ) {
	throw new RuntimeException( 'Saved Global Styles override did not win over generated defaults: ' . wp_json_encode( $effective_styles['color'] ?? array() ) );
}
$footer_template = get_block_template( $slug . '//footer', 'wp_template_part' );
if ( ! $footer_template || ! str_contains( $footer_template->content, 'Client footer preserved' ) ) {
	throw new RuntimeException( 'Saved template-part override did not survive or take precedence.' );
}
$file_default = json_decode( file_get_contents( get_theme_file_path( 'theme.json' ) ), true )['styles']['color']['background'];
$drift = array( 'phase' => $phase, 'generated_background_default' => $file_default, 'saved_background_override' => '#101820', 'effective_background' => $effective_styles['color']['background'], 'saved_footer_override' => true, 'resolution' => 'retain-client-overrides' );
$css = file_get_contents( get_theme_file_path( 'assets/css/stbb-content.css' ) );
if ( str_contains( $css, 'STBB_FIXTURE_UPDATED' ) !== ( $phase === 'updated' ) ) {
	throw new RuntimeException( 'Theme file revision did not match update phase.' );
}
if ( count( parse_blocks( $page->post_content ) ) < 4 ) {
	throw new RuntimeException( 'Saved page did not retain all four patterns.' );
}
$rendered = do_blocks( $page->post_content );
if ( ! str_contains( $rendered, 'Tell your story' ) || ! str_contains( $rendered, 'Get in touch' ) ) {
	throw new RuntimeException( 'Published core-block content failed to render.' );
}
echo 'STBB_PROBE_OK ' . $phase . ' ' . get_bloginfo( 'version' ) . ' ' . PHP_MAJOR_VERSION . '.' . PHP_MINOR_VERSION . PHP_EOL;
echo 'STBB_PAGE_ID ' . $page->ID . PHP_EOL;
echo 'STBB_DRIFT ' . wp_json_encode( $drift ) . PHP_EOL;
